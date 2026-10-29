# Test log: does the skill produce a page at the level of an award-winning site?

Method: an independent builder agent builds a landing page for an invented SaaS ("Quillon", cash-flow forecasting for creative studios)
using only `SKILL.md`. A separate critic agent (not the builder) compares screenshots of the build with screenshots of a real,
award-listed SaaS site at 1440, 768 and 390 px and scores both per criterion. After each round the general lessons go into the skill
and the build is repeated from scratch. Scores are the critic's, on stills only (motion, pricing and footer were not always visible).

| Round | Skill version | Critic total (build) | Verdict | Main gaps |
|---|---|---|---|---|
| 1 | v1 | about 5.0 | no | empty hero at scroll 0, no colour, alert colour with nothing wrong, system font, dead links |
| 2 | v3 | about 6.5 | no | hero is a diagram, colour world only on paper, quiet page is static, small finish errors (a weekday off by one) |
| 3 | v4 | about 7.5 to 8.0 (reference about 7.9) | yes, barely | hero has material but no world, rhythm at the edges, sticky bar vs section tint |
| 4 | v5 | 8.0 (reference 8.2) | no, barely | hero material (a flat vector fill is not material), colour atmosphere (flat tonal blocks), no own form language; gains per round now flattening (+1, +1, +0.5) |

What the skill improved between rounds: start state of a scroll hero, measurable colour world, honest forms and working links,
a real security section for products that touch money, self-hosted display font, two secondary reveals, a finish list.
Not yet verified: motion in a real browser by the critic, pricing and footer, and other categories than SaaS.

After round 4 the skill is v6 (flat fill is zero material, atmosphere per tonal block, one locked form language, mandatory second voice).
The critic's own conclusion: more checklists no longer help; the remaining gap is hero material and colour atmosphere, which in practice
asks for a real canvas or 3D layer. Round 5 has not been run.
