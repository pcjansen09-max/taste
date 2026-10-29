---
name: taste
description: Gives an AI design judgement for websites. Use before designing or building any landing page, product site or hero, and when a page looks like generic AI output. Provides measured numbers from high-end sites, a design process, an anti-slop list and a verification step.
---

# Taste: how to design a website that does not look like AI output

This skill replaces guessing with measurement. The numbers below come from automatically measuring 46 live,
award-level sites (computed styles, not screenshots; see `scripts/extract.py` and `data/aggregate.json`).
They are *ranges to land inside*, not a template to copy. Never copy another site's text, images, code or layout;
learn the decisions, make your own.

## 1. The process (do these in order)

1. **One idea.** Write one sentence: what is the single memorable thing about this brand, and which visual
   decision carries it (a material, a motion, a type voice, a 3D object, a colour world)? Everything else serves it.
   If you cannot say it in one sentence you are about to make a template.
2. **Pick a voice, then constrain.** Two type families at most (one display, one text; a single family used
   at two very different sizes also works). One accent colour. Neutrals that are *not* pure white or pure black.
3. **Fix the rhythm before the content.** An 8 px base; section padding 96 to 140 px on desktop; one content
   container; one grid. Whitespace is the main luxury signal.
4. **Plan the motion, one hero moment.** Choose exactly one thing that moves with intent (a scroll-linked
   sequence, a 3D/canvas object, a video, a type reveal). Everything else is quiet. Motion explains, it does not decorate.
5. **Write the copy first**, short and concrete (see "Copy"). Design around real words, never "Lorem" or "Revolutionize your workflow".
6. **Build, then verify with numbers and eyes** (section 6). Iterate at least twice; the first build is never the one to ship.

## 2. Measured ranges (46 award-level sites, 1440 px wide)

| Decision | Typical (median) | Range worth landing in (p25 to p75) |
|---|---|---|
| Hero headline size | 2.5 vw (about 37 px) | 1.3 to 5.2 vw; statement heroes go 6 to 8 vw |
| Hero headline weight | 400 | 400 to 600. Big type is usually regular or medium, not bold |
| Hero headline line-height | 1.07 | 1.0 to 1.2 (tight) |
| Hero headline words | 3 | 2 to 9. Short |
| Headline in capitals | 34 % of sites | a stylistic choice, only with tracking |
| Body text | 15 px, line-height about 1.25 to 1.5 | 13 to 18 px |
| Page background | 41 % dark, 59 % light | never pure #000 or #fff; use near-black or warm off-white |
| First screen | one full viewport tall (1.0 vh) | hero fills the screen, content below invites scroll |
| Section vertical padding | about 108 px | 72 to 136 px |
| Page length | about 6 screens | 3 to 11 |
| Fonts per page | 2 | 1 to 3 |
| UI transitions | 320 ms | 160 to 500 ms |
| Easing | exponential ease-out (`cubic-bezier(0.16,1,0.3,1)`, `(0.22,1,0.36,1)`, `(0.23,1,0.32,1)`) or `(0.4,0,0.2,1)` | never default `ease` or `linear` for UI |

Technique prevalence on the same sites: smooth scroll (Lenis or similar) 54 %, WebGL canvas 52 % (Three.js 43 %),
any `<canvas>` 65 %, video 48 %, sticky or pinned sections 39 %. High-end is rarely "more effects": it is *one*
effect done with restraint plus a calm layout.

## 3. Anti-slop list (if you catch yourself doing these, stop and decide again)

- Purple-to-blue gradient hero, gradient text on every heading, glowing blobs behind the headline.
- A row of three identical rounded cards with an emoji or stock icon on top.
- Everything centred, everything the same width, everything the same radius and shadow.
- A fake "Trusted by" logo strip; invented testimonials; stock photos of people at laptops.
- Copy such as "Revolutionize", "supercharge", "seamless", "unlock", "all-in-one platform", "powered by AI".
- Inter or system font at default weights with no scale contrast; headline and body only 1.5x apart.
- Pure #fff on pure #000, or pale grey text that fails contrast (keep text at 4.5:1 or better).
- Animation on everything (parallax on every block, bouncing icons, fade-in on every element).
- Default `ease`/`linear` transitions; hover states that only change opacity.
- A hero image or 3D object that has nothing to do with what the product does.
- Dead ends: a call to action or link that goes nowhere (`href="#"`), a form that does nothing, footer links to pages that do not exist. Every button must work or be removed.
- An alert colour (red, amber) visible when nothing is wrong. Warning colours appear only where the user must act.
- Copy that contradicts itself: a weekday that does not match the date, "per studio, not per seat" above prices by headcount, figures that do not add up. Compute every number from one source.

## 4. What makes it feel expensive

- **Scale contrast.** Huge type next to small, quiet type. Hierarchy comes from size, not from bold and colour.
- **Restraint in colour.** One accent used in a few places, so it means something.
- **Real content.** Specific numbers, product screenshots that are real UI, a point of view.
- **Alignment and space.** Consistent left edges, consistent gaps, room around the hero.
- **Motion with weight.** Expo-out easing, 400 to 800 ms for reveals, staggered 40 to 80 ms per line, scroll-linked only where it explains something.
- **A detail nobody asked for.** One small crafted thing (a custom cursor state, a type detail, a counter that actually counts).

## 5. Trust and completeness

- If the product touches money, accounts or personal data (banking, payroll, health, identity), the page needs a visible
  security and integrations block: what access is requested, read-only or not, where data lives, how to revoke. One sentence in
  a step description is not enough.
- A complete page has: hero, how it works, the product shown as real UI (drawn in HTML/CSS/SVG or a real screenshot, never
  stock), proof or pricing, one closing call to action, a footer with working links. If a link has no real page yet, drop it.
- The product's own data can be the hero: a real chart that draws itself beats a decorative blob. Make the hero show what the product knows.

## 6. Copy

Lead with what the product does, for whom, in the customer's words. Verbs and numbers over adjectives.
One call to action per screen. Microcopy has personality but never jokes at the user's expense.

## 7. Verify (required)

1. Screenshot your build at 1440, 768 and 390 px, at the top and after scrolling to 25, 50, 75 %.
1b. Fonts: name a fallback stack so the voice survives on every OS (for example a serif display stack plus a system sans), or self-host one open-licence font if the brief allows files.
2. Run `python scripts/extract.py out YOUR_URL` and compare with `data/aggregate.json`: headline vw, weight,
   line-height, section padding, transition ms, easing, fonts per page. Outside the range is allowed only if you can say why.
3. Check against the anti-slop list item by item.
4. Check accessibility and robustness: contrast 4.5:1 for all text (including small grey labels), visible focus states,
   `prefers-reduced-motion` turns the hero moment into a still, no horizontal scroll at 320 to 1920 px, nothing cut off at 200 % zoom
   or in a 620 px tall window (a pinned hero then becomes a normal section showing the final state), every link and button works.
5. Ask someone (or another model) who did not build it to compare it to a real high-end site in the same category and say where it falls short. Fix those points and run the check again.

## 8. Using references

References are links to live sites in the library (not copies). Look at how they solve spacing, type and motion, then
close the tab and design from the principles. Do not rebuild a reference, and do not reuse its text, images, code or assets.
