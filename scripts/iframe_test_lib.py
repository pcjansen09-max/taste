"""Test per site of hij in een iframe laadt (geen X-Frame-Options/frame-ancestors-blokkade) en toont dan hoeveel inhoud.
Gebruik: python scripts/iframe_test.py UITVOER.jsonl URL [URL ...]"""
import asyncio, json, sys
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright

async def een(pw, url, uit):
    b = await pw.chromium.launch(args=["--enable-unsafe-swiftshader"])
    rec = {"url": url}
    try:
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        p = await ctx.new_page()
        fouten = []
        p.on("console", lambda m: fouten.append(m.text[:140]) if "frame" in m.text.lower() and ("refused" in m.text.lower() or "blocked" in m.text.lower()) else None)
        await p.set_content(f'<html><body style="margin:0"><iframe id="f" src="{url}" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox" referrerpolicy="no-referrer" style="width:1440px;height:900px;border:0"></iframe></body></html>')
        await p.wait_for_timeout(9000)
        fr = [f for f in p.frames if f != p.main_frame]
        if not fr:
            rec.update(werkt=False, reden="geen frame")
        else:
            f = fr[0]
            try:
                tekst = await f.evaluate("(document.body && document.body.innerText || '').trim().length")
                titel = await f.evaluate("document.title")
                rec.update(frame_url=f.url[:80], tekst=tekst, titel=titel[:60])
                rec["werkt"] = bool((tekst > 80 or await f.evaluate("document.querySelectorAll('canvas').length > 0")) and not f.url.startswith("chrome-error") and "unsupported" not in f.url)
                if not rec["werkt"]: rec["reden"] = "leeg of foutpagina"
            except Exception as e:
                rec.update(werkt=False, reden="frame onleesbaar: " + str(e)[:80])
        rec["console"] = fouten[:2]
    except Exception as e:
        rec.update(werkt=False, reden=str(e)[:100])
    finally:
        await b.close()
    uit.open("a").write(json.dumps(rec) + "\n")
    print(("OK   " if rec.get("werkt") else "NEE  ") + url, rec.get("reden", ""), flush=True)

async def main():
    uit = Path(sys.argv[1]); sem = asyncio.Semaphore(4)
    async with async_playwright() as pw:
        async def lim(u):
            async with sem: await een(pw, u, uit)
        await asyncio.gather(*(lim(u) for u in sys.argv[2:]))
asyncio.run(main())
