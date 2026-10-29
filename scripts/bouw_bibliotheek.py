"""Bouwt de nieuwe DeltaOS-bibliotheek: 50 high-end sites als LIVE iframe-referentie (geen kopie), elk als complete site en als hero.

1. Kiest 50 sites die echt in een iframe laden (data/iframe*.jsonl, gemaakt door scripts/iframe_test.py).
2. Maakt per site een kleine miniatuur (eerste scherm, 720x450) voor de kaart.
3. Zet de OUDE catalogus in het Archief (nooit weg) en schrijft een nieuwe catalogue.json met alleen deze referenties.
Gebruik: python scripts/bouw_bibliotheek.py
"""
import asyncio, hashlib, json, re, shutil, time
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
from playwright.async_api import async_playwright

HIER = Path(__file__).resolve().parent.parent
CAT = Path.home() / "delta/src/core/deltaos/venster/catalogue"
ARCHIEF = Path.home() / "secondbrain/zakelijk/Archief/DeltaOS-componentenbibliotheek-2026-10-29"
UIT_NIET = ("trevornoah", "paulkalkbrenner", "noartmusic", "mosbyfiles")   # persoonsmerken en muziek: geen ontwerpreferentie voor ons werk

def kies(n=50):
    ok = []
    for f in ("iframe1.jsonl", "iframe2.jsonl"):
        for l in (HIER / "data" / f).read_text().splitlines():
            r = json.loads(l)
            if r.get("werkt") and not any(x in r["url"] for x in UIT_NIET) and r["url"] not in [o["url"] for o in ok]:
                ok.append(r)
    return ok[:n]

def slug(url):
    p = urlparse(url)
    return re.sub(r"[^a-z0-9]+", "-", (p.netloc.replace("www.", "") + (p.path if len(p.path) > 1 else "")).lower()).strip("-")[:40]

async def thumbs(sites):
    sem = asyncio.Semaphore(4)
    async with async_playwright() as pw:
        async def een(s):
            async with sem:
                b = await pw.chromium.launch(args=["--enable-unsafe-swiftshader"])
                try:
                    p = await (await b.new_context(viewport={"width": 1440, "height": 900})).new_page()
                    await p.goto(s["url"], wait_until="load", timeout=60000)
                    await p.wait_for_timeout(5000)
                    try:
                        await p.evaluate("""() => { const t=/^(accept|accepteer|alles accepteren|accept all|allow all|akkoord|agree|ok)$/i; for (const e of document.querySelectorAll('button,a,[role=button]')) { if (t.test((e.innerText||'').trim())) { e.click(); break; } } }""")
                    except Exception:
                        pass
                    await p.wait_for_timeout(1500)
                    png = await p.screenshot(type="png")
                    im = Image.open(BytesIO(png)).convert("RGB")
                    lum = sum(im.resize((24, 15)).convert("L").getdata()) / (24 * 15)
                    s["dark"] = lum < 90
                    im.resize((720, 450)).save(CAT / "thumbs" / f"ref-{s['slug']}.jpg", quality=80)
                    s["thumb_ok"] = True
                except Exception as e:
                    s["thumb_ok"] = False
                    s["thumb_fout"] = str(e)[:80]
                finally:
                    await b.close()
        await asyncio.gather(*(een(s) for s in sites))

def item(s, hero):
    host = urlparse(s["url"]).netloc.replace("www.", "")
    titel = (s.get("titel") or host).strip()
    titel = re.sub(r"\s+", " ", titel)[:60] or host
    return {
        "id": f"{'hero' if hero else 'site'}-{s['slug']}",
        "title": titel if not hero else f"{titel} (hero)",
        "subtitle": (f"Het eerste scherm van {host}, live." if hero else f"{host}, complete high-end site, live."),
        "category": "Hero's" if hero else "Complete sites",
        "source": "Referentie",
        "interaction": "Scrollen en klikken" if not hero else "Eerste scherm",
        "dark": bool(s.get("dark")),
        "embed": "site", "view": "hero" if hero else "full",
        "preview": s["url"], "thumbnail": f"/catalogue/thumbs/ref-{s['slug']}.jpg",
        "sources": [{"component": host, "sha256": hashlib.sha256(s["url"].encode()).hexdigest(), "code": "", "url": s["url"]}],
        "license": "Referentie (link naar de live site)", "license_url": "/catalogue/LICENSES.txt",
        "provenance": f"Live site van de makers ({host}), hier ingebed. Geen kopie en geen code van ons; alleen om van te leren en naar te verwijzen. Niet gebruiken als bron voor klantwerk.",
        "review": "Referentie, niet gekopieerd", "tags": ["referentie", "high-end", "awwwards", host],
        "template_kind": "external-reference",
    }

def main():
    sites = kies(50)
    for s in sites:
        s["slug"] = slug(s["url"])
    (CAT / "thumbs").mkdir(exist_ok=True)
    asyncio.run(thumbs(sites))
    goed = [s for s in sites if s.get("thumb_ok")]
    ARCHIEF.mkdir(parents=True, exist_ok=True)
    oud = CAT / "catalogue.json"
    if not (ARCHIEF / "catalogue.json").exists():
        shutil.copy2(oud, ARCHIEF / "catalogue.json")
    items = [item(s, False) for s in goed] + [item(s, True) for s in goed]
    oud.write_text(json.dumps({"version": 1, "items": items}, ensure_ascii=False, indent=1))
    (HIER / "data" / "bibliotheek.json").write_text(json.dumps([{k: s[k] for k in ("url", "slug", "titel", "dark")} for s in goed], indent=1))
    print(len(goed), "sites,", len(items), "items; mislukte miniaturen:", [s["url"] for s in sites if not s.get("thumb_ok")])

main()
