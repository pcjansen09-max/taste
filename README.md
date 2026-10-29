# taste

A skill that gives an AI design judgement for websites. Instead of guessing, it works from numbers measured on 46 live,
award-level sites (computed styles, not screenshots or copied code) plus a design process, an anti-slop list and a verification step.

- `SKILL.md`: the skill itself (works as a Claude Code skill; the content is plain Markdown for any agent)
- `data/aggregate.json`: the measured distributions (headline scale, weight, spacing, timing, easing, techniques)
- `data/sites.txt`: the public sites that were measured (links only)
- `scripts/extract.py`: measures one live site; `scripts/analyze.py`: aggregates many
- `scripts/iframe_test.py`: checks whether a site can be embedded as a live reference

Nothing here copies another site's text, images, code or layout. The measurements are facts (sizes, durations, counts).
MIT licensed.

## Does it work?

See `docs/TEST-LOG.md`: three rounds of "build with the skill, judge against an award-listed site, improve the skill".
The latest build scored about on par with the reference on stills; it is not yet proven for other site categories.
