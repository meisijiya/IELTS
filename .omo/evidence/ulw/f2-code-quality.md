=== F2 Code Quality — 2026-08-16 19:20:36 UTC ===

## Sampled topics

### 1. p1-hometown (Part 1 required, 15 Qs)
- FC features: PASS — discourse markers throughout: "honestly" (q1,q5), "The thing is" (q2), "Well" (q3), "actually" (q4,q14), "I mean" (q6), "To be honest" (q7), "On top of that" (q8), "you know" (q12), "Oh, definitely" (q12), "Hmm" (q15). Long turns: 2–3 sentences per answer, willing to extend (q2, q10, q12).
- LR features: PASS — less-common vocab: "first-tier city", "skyscrapers", "ferris wheel", "special economic zone", "fishing village", "global city", "migrants", "attachment", "infrastructure", "within easy reach", "chase their dreams", "transformation fascinates me". Paraphrase: "huge city, one of the biggest in China" (q2).
- GRA features: PASS — flexible complex structures: conditional "If I had to pick something, it'd be the cost of living, which is pretty high" (q9), participial "Walking around the streets, I often feel..." (q12), absolute "with companies like Tencent based there" (q10). Mostly accurate.
- Pitfall scan: PASS — no learn knowledge / open light / big traffic / although...but / because...so same-sentence / a+uncountable / "As for me" templates.
- Severity: none

### 2. p1f-cars (Part 1 high-freq, 5 Qs)
- FC features: PASS — "to be honest" (q2,q3), "honestly" (q4), "I mean" (q5), "Definitely" (q3). Long turns 2–3 sentences each.
- LR features: PASS — "SUVs", "plenty of space", "behind the wheel", "restless", "traffic jam", "street life", "spot interesting little scenes", "stand out". Paraphrase: "I'd rather watch the street life... than stare at my phone" (q4).
- GRA features: PASS — relative + because: "They have plenty of space, which matters to me because I'm quite tall" (q2); compound-complex "I mean, white and black cars are everywhere anyway, so colour doesn't really stand out anymore" (q5). Mostly accurate.
- Pitfall scan: PASS — "traffic jam" used correctly (not "big traffic"); no although...but / because...so same-sentence (q1 "because" alone, no "so").
- Severity: none

### 3. p23-fav-city (Part 2&3 PLACE, cue + 5 P3)
- FC features: PASS — cue (~200 words, full 2-min turn) with signposting: "I'd like to describe", "I suppose you could say", "Actually", "The thing is", "As a result", "Honestly", "All in all". P3: "generally speaking", "That said", "Having said that", "on the whole", "on the other hand". All 4 cue bullets covered (where/how knew/when/why).
- LR features: PASS — "megacity", "concentrate opportunities", "well-paid jobs", "stunning skylines", "heritage", "trendy photo spot", "carry the most weight", "tolerance for crowds", "bustling atmosphere". Paraphrase: "it's not really a city I visited, more the city I grew up in".
- GRA features: PASS — relative clauses "Shenzhen, my home city, which sits right on the southern coast", "There's Qianhai, where you can walk along the sea... and Shenzhen Bay Park, which is great for a relaxing weekend"; conditional "if remote work keeps expanding, some people may choose cheaper, smaller cities". Mostly accurate.
- Pitfall scan: PASS — no learn knowledge / open light / big traffic / although...but / because...so same-sentence / a+uncountable / template openings.
- Severity: none

### 4. p23-child-friend (Part 2&3 PEOPLE, cue + 6 P3)
- FC features: PASS — cue with discourse markers: "I'd like to talk about", "actually", "honestly", "As for what we did together", "Looking back", "Unfortunately". P3: "To be honest", "I mean", "For one thing", "On top of that", "From my perspective", "That said", "Generally speaking". All 4 cue bullets covered (who/met/what did/why liked).
- LR features: PASS — "inseparable", "out of breath", "drifted apart", "sense of security and belonging", "emotional development", "tone of voice", "body language", "complement, rather than replace", "shallower".
- GRA features: PASS — noun clause "The reason I liked him so much was that he was just so much fun to be around"; passive "friendship is built on being together every day"; embedded question "how to enjoy the simple things". Mostly accurate.
- Pitfall scan: PASS — "The main reason is that..." correct (not "reason is because"); "although it will probably keep growing" (p3-4) — although alone, no "but". No learn knowledge / open light / big traffic / a+uncountable.
- Severity: none

### 5. p23-early (Part 2&3 EVENTS, cue + 6 P3)
- FC features: PASS — cue with signposting: "I'd like to describe", "The funny thing is", "As for how I felt", "On one hand... On the other hand", "Looking back". P3: "Having said that", "generally speaking", "Another factor is", "on the whole". All 4 cue bullets covered (when/what/why/felt).
- LR features: PASS — "wide awake", "messing around with some code", "change of pace", "early risers", "lose track of time", "time-sensitive", "out of respect", "consistency", "adapts to a regular routine".
- GRA features: PASS — past perfect "before the sun had even come up"; comparative correlative "the more formal or time-sensitive the occasion, the earlier people should arrive" (p3-3); compound-complex throughout. Mostly accurate.
- Pitfall scan: PASS — no learn knowledge / open light / big traffic / although...but / because...so same-sentence / a+uncountable / template openings.
- Severity: minor — p3-6 `question_en` is placeholder "待补充" (answer present and band-6.5 quality, but question text missing). Data defect, not a language defect; affects 1 of 71 topics.

## HTML validation
- 71 topic pages validated: PASS (python3 HTMLParser, no unclosed-tag errors)
- index.html validated: PASS

## JS validation
- learning-mode.js: PASS — `node --check` clean (no syntax errors). 51-line IIFE; guards for missing elements (`if (!items.length) return`, `if (hideBtn)`), try/catch around localStorage (private-mode safe), keyboard handler ignores INPUT/TEXTAREA/contentEditable. No obvious defects.

## CSS check
- Uses shared tokens: PASS — `var(--green)`, `var(--muted)`, `var(--bg)`, `var(--ink)` used throughout (badges, buttons, cards, search focus).
- No new brand colors: PASS — hardcoded hex values are neutral grays (#777/#555/#666/#888/#aaa/#ccc/#e5e5e5) plus a consistent amber warning palette (#fff8d6/#ecdfa3/#d4a017/#7a5b00/#4a3a00) used only for `.ai-flag` and `.disclaimer`. No hardcoded green/ink/bg/muted brand colors.

=== VERDICT: APPROVE ===
=== done ===