"""Zet de metingen in out/ om in cijfers die een ontwerper (of een AI) kan gebruiken: percentielen en verdelingen."""
import json, statistics as st, sys
from collections import Counter
from pathlib import Path

def pct(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs: return None
    return round(xs[min(len(xs) - 1, int(len(xs) * p))], 3)

def samen(xs):
    return {"n": len([x for x in xs if x is not None]), "p10": pct(xs, .1), "p25": pct(xs, .25), "mediaan": pct(xs, .5), "p75": pct(xs, .75), "p90": pct(xs, .9)}

data = [json.load(open(p)) for p in sorted(Path(sys.argv[1]).glob("*.json"))]
n = len(data)
h1 = [d["h1"] for d in data if d.get("h1")]
body = [t["size"] for d in data for t in (d["typ"].get("p") or [])[:10]]
body_lh = [t["lh"] for d in data for t in (d["typ"].get("p") or [])[:10] if 0.8 < t["lh"] < 3]
h2 = [t["size"] for d in data for t in (d["typ"].get("h2") or [])[:5]]
pads = [x for d in data for row in d.get("padding", []) for x in row[:2] if x >= 24]
dur = [x for d in data for x in d["beweging"].get("duur_ms", []) if 50 <= x <= 3000]
ease = Counter()
for d in data:
    for k, v in d["beweging"].get("easing", []):
        if k not in ("ease", "linear", "ease-in-out", "ease-out", "ease-in"):
            ease[k] += 1
tech = Counter()
for d in data:
    for k, v in d.get("tech", {}).items():
        if v: tech[k] += 1
fam = Counter(f for d in data for f in d.get("fonts", [])[:3])
agg = {
    "aantal_sites": n,
    "h1": {"vw": samen([x["vw"] for x in h1]), "px": samen([x["size"] for x in h1]), "lineheight": samen([x["lh"] for x in h1]),
           "letterspacing_em": samen([x["ls"] for x in h1]), "gewicht": samen([x["weight"] for x in h1]),
           "woorden": samen([x["woorden"] for x in h1]), "uppercase_aandeel": round(sum(1 for x in h1 if x["tt"] == "uppercase") / max(1, len(h1)), 2)},
    "h2_px": samen(h2), "body_px": samen(body), "body_lineheight": samen(body_lh),
    "contrast": samen([d["pixels"]["contrast_bereik"] for d in data if d.get("pixels")]),
    "donker_aandeel": round(sum(1 for d in data if d.get("pixels", {}).get("donker")) / n, 2),
    "hero_hoogte_vh": samen([d["hero"]["hoogte_vh"] for d in data]),
    "pagina_hoogte_vh": samen([d["pagina"]["hoogte_vh"] for d in data]),
    "container_aandeel_breedte": samen([d.get("container") for d in data]),
    "verticale_padding_px": samen(pads),
    "transitieduur_ms": samen(dur),
    "populaire_easing": ease.most_common(8),
    "aantal_lettertypefamilies_per_site": samen([len(set(d.get("fonts", []))) for d in data]),
    "tech_aandeel": {k: round(v / n, 2) for k, v in tech.most_common()},
    "canvas_aandeel": round(sum(1 for d in data if d["canvas"] > 0) / n, 2),
    "video_aandeel": round(sum(1 for d in data if d["video"] > 0) / n, 2),
    "sticky_of_pinned_aandeel": round(sum(1 for d in data if d["sticky"] > 0) / n, 2),
    "eigen_cursor_aandeel": round(sum(1 for d in data if d.get("cursor_eigen")) / n, 2),
    "populaire_fonts": fam.most_common(10),
}
Path("data").mkdir(exist_ok=True)
Path("data/aggregate.json").write_text(json.dumps(agg, indent=1, ensure_ascii=False))
print(json.dumps(agg, indent=1, ensure_ascii=False)[:3500])
