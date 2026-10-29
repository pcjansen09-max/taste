"""Meet de ontwerpkeuzes van een live site: lettertypeschaal, kleur en contrast, witruimte, hero, beweging, 3D en scrolltechniek.

Bewaart alleen getallen en technieknamen, nooit tekst, beelden of ontwerpen van de site zelf.
Gebruik: python scripts/extract.py UITVOERMAP URL [URL ...]
"""
import asyncio, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright

JS = r"""
() => {
  const px = v => parseFloat(v) || 0;
  const rgb = c => { const m = (c || '').match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const contrast = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const vw = innerWidth, vh = innerHeight;
  const visible = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 4 && r.height > 4 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; };
  const bgOf = e => { let n = e; while (n) { const c = rgb(getComputedStyle(n).backgroundColor); if (c && c.a > 0.5) return c; n = n.parentElement; } return {r: 255, g: 255, b: 255, a: 1}; };
  const out = {};
  // typografie
  const typ = {};
  for (const sel of ['h1', 'h2', 'h3', 'p', 'a', 'button', 'li']) {
    const els = Array.from(document.querySelectorAll(sel)).filter(visible).slice(0, 40);
    typ[sel] = els.map(e => { const s = getComputedStyle(e); return {size: px(s.fontSize), weight: parseInt(s.fontWeight) || 400, lh: s.lineHeight === 'normal' ? 1.2 : px(s.lineHeight) / px(s.fontSize), ls: px(s.letterSpacing) / px(s.fontSize), tt: s.textTransform, fam: (s.fontFamily || '').split(',')[0].replace(/["']/g, '').trim()}; });
  }
  out.typ = typ;
  let h1 = Array.from(document.querySelectorAll('h1')).filter(visible)[0];
  if (!h1) {   // geen zichtbare h1: de grootste tekst in het eerste scherm
    let beste = null, grootte = 0;
    for (const e of Array.from(document.querySelectorAll('h1,h2,h3,p,span,div,a')).filter(visible)) {
      const r = e.getBoundingClientRect(); if (r.top > vh || r.bottom < 0) continue;
      if (!(e.innerText || '').trim() || e.children.length > 3) continue;
      const f = px(getComputedStyle(e).fontSize); if (f > grootte && (e.innerText || '').trim().length > 2) { grootte = f; beste = e; }
    }
    if (beste) { h1 = beste; out.h1_terugval = true; }
  }
  if (h1) { const s = getComputedStyle(h1), r = h1.getBoundingClientRect(); out.h1 = {size: px(s.fontSize), vw: px(s.fontSize) / vw * 100, weight: parseInt(s.fontWeight) || 400, lh: s.lineHeight === 'normal' ? 1.2 : px(s.lineHeight) / px(s.fontSize), ls: px(s.letterSpacing) / px(s.fontSize), woorden: (h1.innerText || '').trim().split(/\s+/).filter(Boolean).length, tt: s.textTransform, top: r.top, breedte: r.width / vw}; }
  const body = document.body, bs = getComputedStyle(body);
  const bg = bgOf(body), fg = rgb(bs.color) || {r: 0, g: 0, b: 0};
  out.kleur = {bg: [bg.r, bg.g, bg.b], fg: [fg.r, fg.g, fg.b], contrast: contrast(bg, fg), donker: lum(bg) < 0.2};
  // accent: meest voorkomende verzadigde kleur op knoppen en links
  const acc = {};
  for (const e of Array.from(document.querySelectorAll('a, button')).filter(visible).slice(0, 80)) {
    for (const c of [rgb(getComputedStyle(e).backgroundColor), rgb(getComputedStyle(e).color)]) {
      if (!c || c.a < 0.5) continue;
      const mx = Math.max(c.r, c.g, c.b), mn = Math.min(c.r, c.g, c.b);
      if (mx - mn < 40) continue;
      const k = [c.r, c.g, c.b].map(v => Math.round(v / 16) * 16).join(',');
      acc[k] = (acc[k] || 0) + 1;
    }
  }
  out.accent = Object.entries(acc).sort((a, b) => b[1] - a[1]).slice(0, 3);
  out.fonts = Array.from(new Set(Array.from(document.querySelectorAll('h1,h2,p,a,button')).filter(visible).slice(0, 120).map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim())));
  // layout, hero, witruimte
  const secs = Array.from(document.querySelectorAll('section, main > div, [class*=section i]')).filter(visible).map(e => e.getBoundingClientRect()).filter(r => r.height > vh * 0.3);
  out.secties = secs.length;
  out.hero = {hoogte_vh: secs.length ? secs[0].height / vh : null};
  let scrollH = document.documentElement.scrollHeight;
  for (const e of Array.from(document.querySelectorAll('body, body > *, main, #app, #root, [class*=scroll i], [data-scroll-container]')).slice(0, 60)) {
    const st = getComputedStyle(e);
    if (/(auto|scroll)/.test(st.overflowY) && e.scrollHeight > e.clientHeight * 1.3) scrollH = Math.max(scrollH, e.scrollHeight);
    if (e.getBoundingClientRect().height > scrollH) scrollH = e.getBoundingClientRect().height;
  }
  out.pagina = {hoogte_vh: scrollH / vh, breedte: vw};
  const pad = Array.from(document.querySelectorAll('section, main, header, footer')).filter(visible).slice(0, 30).map(e => { const s = getComputedStyle(e); return [px(s.paddingTop), px(s.paddingBottom), px(s.paddingLeft), px(s.paddingRight)]; });
  out.padding = pad;
  const maxb = Array.from(document.querySelectorAll('main *, section *')).filter(visible).slice(0, 400).map(e => e.getBoundingClientRect().width).filter(w => w < vw - 20 && w > 300);
  out.container = maxb.length ? Math.max(...maxb) / vw : null;
  // beweging
  const dur = [], ease = {}, anim = new Set();
  for (const e of Array.from(document.querySelectorAll('*')).slice(0, 1500)) {
    const s = getComputedStyle(e);
    if (s.transitionDuration && s.transitionDuration !== '0s') for (const d of s.transitionDuration.split(',')) dur.push(px(d) * (d.includes('ms') ? 1 : 1000));
    if (s.transitionTimingFunction && s.transitionDuration !== '0s') for (const t of s.transitionTimingFunction.split(/,(?![^(]*\))/)) { const k = t.trim(); ease[k] = (ease[k] || 0) + 1; }
    if (s.animationName && s.animationName !== 'none') anim.add(s.animationName);
  }
  out.beweging = {transities: dur.length, duur_ms: dur.slice(0, 300), easing: Object.entries(ease).sort((a, b) => b[1] - a[1]).slice(0, 5), keyframes: anim.size};
  out.sticky = Array.from(document.querySelectorAll('*')).filter(e => { const p = getComputedStyle(e).position; return p === 'sticky'; }).length;
  out.fixed = Array.from(document.querySelectorAll('*')).filter(e => getComputedStyle(e).position === 'fixed').length;
  out.canvas = document.querySelectorAll('canvas').length;
  out.video = document.querySelectorAll('video').length;
  out.svg = document.querySelectorAll('svg').length;
  out.afbeeldingen = document.images.length;
  const w = window;
  out.tech = {gsap: !!w.gsap, scrolltrigger: !!w.ScrollTrigger || !!(w.gsap && w.gsap.core && w.ScrollTrigger), lenis: !!w.Lenis || !!document.querySelector('.lenis'), three: !!w.THREE || !!document.querySelector('canvas[data-engine*=three]'), locomotive: !!document.querySelector('[data-scroll-container],[data-scroll]'), framer: !!document.querySelector('[data-framer-name],[data-framer-component-type]'), webflow: !!document.querySelector('html[data-wf-site]'), nextjs: !!w.__NEXT_DATA__ || !!document.querySelector('#__next'), barba: !!w.barba, splitting: !!document.querySelector('[data-splitting],.split-text,[class*=split i]'), lottie: !!w.lottie, rive: !!document.querySelector('canvas[data-rive]'), webgl: Array.from(document.querySelectorAll('canvas')).some(c => { try { return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } })};
  out.cursor_eigen = Array.from(document.querySelectorAll('body, a, button')).slice(0, 20).some(e => getComputedStyle(e).cursor === 'none');
  return out;
}
"""

async def een(pw, url, uit):
    naam = re.sub(r"[^a-z0-9]+", "-", (urlparse(url).netloc + urlparse(url).path).lower()).strip("-")[:60]
    pad = uit / f"{naam}.json"
    if pad.exists():
        return
    b = await pw.chromium.launch(args=["--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader"])
    try:
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        p = await ctx.new_page()
        await p.goto(url, wait_until="load", timeout=60000)
        await p.wait_for_timeout(4000)
        # cookiemuur
        try:
            await p.evaluate("""() => { const t=/^(accept|accepteer|alles accepteren|accept all|allow all|akkoord|agree|ok)$/i; for (const e of document.querySelectorAll('button,a,[role=button]')) { if (t.test((e.innerText||'').trim())) { e.click(); break; } } }""")
        except Exception:
            pass
        await p.wait_for_timeout(1500)
        for _ in range(12):
            await p.mouse.wheel(0, 700)
            await p.wait_for_timeout(250)
        await p.evaluate("window.scrollTo(0, 0)")
        await p.wait_for_timeout(1500)
        data = await p.evaluate(JS)
        try:
            from io import BytesIO
            from PIL import Image
            png = await p.screenshot(type="png")
            im = Image.open(BytesIO(png)).convert("RGB").resize((96, 60))
            px = list(im.getdata())
            lumv = lambda c: 0.2126 * (c[0] / 255) ** 2.2 + 0.7152 * (c[1] / 255) ** 2.2 + 0.0722 * (c[2] / 255) ** 2.2
            ls = sorted(lumv(c) for c in px)
            data["pixels"] = {"lum_mediaan": ls[len(ls) // 2], "lum_p10": ls[len(ls) // 10], "lum_p90": ls[len(ls) * 9 // 10],
                              "donker": ls[len(ls) // 2] < 0.2, "contrast_bereik": (ls[len(ls) * 9 // 10] + 0.05) / (ls[len(ls) // 10] + 0.05)}
        except Exception as f:
            data["pixels_fout"] = str(f)[:80]
        data["url"] = url
        pad.write_text(json.dumps(data))
        print("ok  ", url, flush=True)
    except Exception as f:
        print("fout", url, str(f)[:100].replace("\n", " "), flush=True)
        pad.with_suffix(".fout").write_text(str(f)[:300])
    finally:
        await b.close()

async def main():
    uit = Path(sys.argv[1]); uit.mkdir(parents=True, exist_ok=True)
    urls = sys.argv[2:]
    sem = asyncio.Semaphore(3)
    async with async_playwright() as pw:
        async def lim(u):
            async with sem:
                await een(pw, u, uit)
        await asyncio.gather(*(lim(u) for u in urls))

asyncio.run(main())
