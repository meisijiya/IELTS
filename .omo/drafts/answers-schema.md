# Answers JSON Schema — IELTS Speaking Bank (2026 May-Aug)

## File

`docs/speaking/data/answers.json`

## Top-level shape

```ts
type AnswersFile = {
  meta: {
    source_pdf: string;          // PDF filename
    source_pages: number;        // 41
    bank_period: string;         // "2026 May–Aug"
    extracted_on: string;        // ISO date
    topic_count: number;         // 71 (see Note A)
    schema_version: string;      // "1.0.0"
    notes: string[];             // discrepancy / TODO flags
  };
  topics: Topic[];
};
```

## `Topic` shape (per entry in `topics`)

```ts
type Topic = {
  id: string;                    // e.g. "p1-hometown", "p23-fav-city"
  slug: string;                  // same as id, used for filename
  title_zh: string;              // 中文标题
  title_en: string;              // English title (from PDF cue card / index)
  part: "p1-required" | "p1-high-freq" | "p23";
  category: "place" | "object" | "event" | "abstract" | "people" | "place-p23" | "object-p23" | "event-p23";
  is_required: boolean;          // true only for the 5 Part 1 required
  is_ai_supplemented: boolean;   // true if experience was fabricated (see questionnaire "没有" items)
  pdf_pages: number[];           // source PDF page numbers (1-indexed)
  cue_card?: CueCard;            // Part 2&3 topics only
  questions: Question[];
};
```

### `CueCard` shape (Part 2&3 topics only)

```ts
type CueCard = {
  bullets_en: string[];          // 3-4 "You should say" bullets from PDF
  bullets_zh?: string[];         // optional Chinese translations
};
```

### `Question` shape

```ts
type Question = {
  id: string;                    // e.g. "q1", "q2"; "cue" for the cue-card prompt; "p3-1" for Part 3
  question_en: string;           // verbatim from PDF
  question_zh?: string;          // empty for Part 1 (PDF has no Chinese); filled for Part 2 cue cards by translation
  answer_en: string;             // "" — filled by Wave 2-7 workers
  answer_hint_zh: string;        // "" — filled by Wave 2-7 workers
  ai_supplemented: boolean;      // true if answer relies on AI-supplemented experience
};
```

## Field population rules

| Field | Source |
|---|---|
| `id` | Stable slug derived from topic title; see slug table in Note B |
| `title_en` | PDF index title for Part 1; full cue-card phrase for Part 2&3 (e.g. "Describe your favorite city that you have visited") |
| `title_zh` | Translated; matches user's questionnaire language |
| `part` | "p1-required" (5) \| "p1-high-freq" (27) \| "p23" (39) |
| `category` | See category rules below |
| `is_required` | `true` for the 5 Part 1 required topics |
| `is_ai_supplemented` | `true` if any answer in this topic relies on AI-supplemented experience (see experience-questionnaire.md "没有" items) |
| `pdf_pages` | Page numbers where this topic's questions appear in the PDF (e.g. Hometown is on p.5–7 → `[5,6,7]`) |
| `cue_card.bullets_en` | "You should say" bullets from PDF for Part 2&3 topics |
| `questions` | For Part 1: array of 4-17 sub-questions (varies by topic). For Part 2&3: includes one synthetic "cue" question (the cue card prompt), then the Part 3 sub-questions. |

### Category rules

| Part | Category values |
|---|---|
| p1-required | (n/a — uses "place" / "abstract" loosely; "home" gets "object") |
| p1-high-freq | "place" (Parks/Outer space/Building), "object" (14 items), "event" (7 items), "abstract" (3 items) |
| p23 | "place-p23" (PLACE 6), "people" (PEOPLE 11), "object-p23" (OBJECTS 10), "event-p23" (EVENTS 12) |

> Category is duplicated as `part` + `category` so a single "place" filter doesn't accidentally match both Part 1 PLACE and Part 2&3 PLACE. (e.g. `p1-high-freq`+`place` vs `p23`+`place-p23`.)

## `is_ai_supplemented` — what does it mean?

`true` when the user's experience-questionnaire marks this topic as "没有" (no experience) and the answer therefore relies on AI-supplemented material. Reference: `.omo/drafts/experience-questionnaire.md`.

Topics marked `true` based on F2/F4/F7/F8/F9/F10/F11/F12 in the questionnaire + G1/G9/G10/G16:
- Part 2&3 PEOPLE: plant-grower, child-artist, self-learner, famous-person, helper, smart-solver, nature-lover (7 of 11)
- Part 2&3 OBJECTS: overspent-item (1 of 10)
- Part 2&3 EVENTS: important-decision, gave-advice, bad-music-event (3 of 12)
- Part 2&3 PLACE: boring-place (1 of 6)

## Worked example

```json
{
  "id": "p1-hometown",
  "slug": "p1-hometown",
  "title_zh": "家乡",
  "title_en": "Hometown",
  "part": "p1-required",
  "category": "place",
  "is_required": true,
  "is_ai_supplemented": false,
  "pdf_pages": [5, 6, 7],
  "questions": [
    {
      "id": "q1",
      "question_en": "Where is your hometown?",
      "question_zh": "",
      "answer_en": "",
      "answer_hint_zh": "",
      "ai_supplemented": false
    }
  ]
}
```

```json
{
  "id": "p23-fav-city",
  "slug": "p23-fav-city",
  "title_zh": "描述你最喜欢的一座城市",
  "title_en": "Describe your favorite city that you have visited",
  "part": "p23",
  "category": "place-p23",
  "is_required": false,
  "is_ai_supplemented": false,
  "pdf_pages": [16],
  "cue_card": {
    "bullets_en": [
      "Where it is",
      "How you knew it",
      "When you visited it",
      "And explain why it is your favourite city"
    ],
    "bullets_zh": [
      "它在哪里",
      "你怎么知道它的",
      "你什么时候去的",
      "并解释为什么它是你最喜欢的城市"
    ]
  },
  "questions": [
    {
      "id": "cue",
      "question_en": "Describe your favorite city that you have visited.",
      "question_zh": "描述你去过的最喜欢的一座城市。",
      "answer_en": "",
      "answer_hint_zh": "",
      "ai_supplemented": false
    },
    {
      "id": "p3-1",
      "question_en": "Which is more suitable for young people, urban life or rural life, and which is more suitable for old people?",
      "question_zh": "",
      "answer_en": "",
      "answer_hint_zh": "",
      "ai_supplemented": false
    }
  ]
}
```

## Validation rules (Wave 8 verification script)

1. `python -m json.tool docs/speaking/data/answers.json` must exit 0.
2. `len(d["topics"]) == 71` (see Note A).
3. Every `Topic` has all required fields populated (`id`, `slug`, `title_zh`, `title_en`, `part`, `category`, `is_required`, `is_ai_supplemented`, `pdf_pages`, `questions`).
4. Every `Question` has `id`, `question_en`, `answer_en`, `answer_hint_zh`, `ai_supplemented`.
5. Part 2&3 topics have `cue_card` with `bullets_en` array (length 3 or 4).
6. Part 1 topics do NOT have `cue_card`.
7. Slug uniqueness: `set(t["id"] for t in topics) == set(t["slug"] for t in topics)` and `len == 71`.
8. Question ID uniqueness within each topic.
9. `part` is one of `{"p1-required", "p1-high-freq", "p23"}`.
10. `category` is one of `{"place", "object", "event", "abstract", "people", "place-p23", "object-p23", "event-p23"}` — and `p23` topics use only the `*-p23` variants.

## Note A — Topic count discrepancy (71 vs 73)

- Plan (`ielts-speaking-bank.md`) says **73** total = 5 required + 29 high-freq + 39 P23.
- Task spec also says **73**.
- The questionnaire summary also says "Part 1 高频：29" but lists the breakdown `PLACE 3 + OBJECT 14 + EVENT 7 + ABSTRACT 3 = 27`.

**Actual count from the PDF (May-Aug 2026 edition) is 71**:
- Part 1 required: 5 ✓
- Part 1 high-frequency: 27 (= 3 PLACE + 14 OBJECT + 7 EVENT + 3 ABSTRACT, per PDF index)
- Part 2&3: 39 (= 6 PLACE + 11 PEOPLE + 10 OBJECTS + 12 EVENTS, per PDF index)

The "29" number appears to be a counting error that propagates through the plan + questionnaire + task spec. **This file ships 71 topics matching the PDF verbatim** — no fabricated topics are added to hit 73. If the user wants exactly 73, two topics need to be specified (likely candidates from common IELTS Part 1 banks: "Weather", "Daily routine" — both would need to be marked `is_ai_supplemented: true`).

## Note B — Slug table (id ↔ slug, both equal)

### Part 1 required (5)
| id / slug | title_en |
|---|---|
| `p1-hometown` | Hometown |
| `p1-work` | Work or Studies |
| `p1-home` | Home/Accommodation |
| `p1-area` | The area you live in |
| `p1-city` | The city you live in |

### Part 1 high-frequency (27)
| id / slug | title_en | category |
|---|---|---|
| `p1f-parks` | Parks | place |
| `p1f-outer-space` | Outer space and stars | place |
| `p1f-building` | Building | place |
| `p1f-science` | Science | object |
| `p1f-cars` | Cars | object |
| `p1f-teachers` | Teachers | object |
| `p1f-social-media` | Social media | object |
| `p1f-watch` | Watch | object |
| `p1f-websites` | Websites | object |
| `p1f-mirrors` | Mirrors | object |
| `p1f-gifts` | Gifts | object |
| `p1f-pets` | Pets and Animals | object |
| `p1f-food` | Food | object |
| `p1f-sports-team` | Sports team | object |
| `p1f-scenery` | Scenery | object |
| `p1f-views` | Views | object |
| `p1f-childhood` | Childhood activities | object |
| `p1f-shopping` | Shopping | event |
| `p1f-singing` | Singing | event |
| `p1f-life-stages` | Life stages | event |
| `p1f-morning` | Morning time | event |
| `p1f-reading` | Reading | event |
| `p1f-walking` | Walking | event |
| `p1f-typing` | Typing | event |
| `p1f-tidiness` | Tidiness | abstract |
| `p1f-music` | Music | abstract |
| `p1f-hobby` | Hobby | abstract |

### Part 2&3 (39)
| id / slug | title_en (cue card) | category |
|---|---|---|
| `p23-fav-city` | Describe your favorite city that you have visited | place-p23 |
| `p23-boring` | Describe a boring place | place-p23 |
| `p23-tall` | Describe a tall building you like or dislike | place-p23 |
| `p23-interest-bldg` | Describe an interesting building | place-p23 |
| `p23-famous-city` | Describe a city that you think is very interesting/famous | place-p23 |
| `p23-nanning` | Describe a city you enjoyed visiting | place-p23 |
| `p23-child-friend` | Describe a friend from your childhood | people |
| `p23-business` | Describe a person you know who has a successful business | people |
| `p23-plants` | Describe a person who loves to grow plants | people |
| `p23-medical` | Describe a person you know who would like to choose a career in the medical field | people |
| `p23-planning` | Describe a person who makes plans a lot and is good at planning | people |
| `p23-child-art` | Describe a child who loves drawing/painting | people |
| `p23-self-learn` | Describe one of your friends who learned something without a teacher | people |
| `p23-famous` | Describe a famous person you would like to meet | people |
| `p23-helper` | Describe a person who often helps others | people |
| `p23-smart` | Describe a person who solved a problem in a smart way | people |
| `p23-nature` | Describe a person who likes to look after the natural world | people |
| `p23-law` | Describe a new law you would like to introduce in your country | object-p23 |
| `p23-changed-plan` | Describe a plan that you had to change recently | object-p23 |
| `p23-video` | Describe an interesting video | object-p23 |
| `p23-movie` | Describe a movie you watched and enjoyed recently | object-p23 |
| `p23-tech` | Describe a piece of technology (not a phone) that you would like to own | object-p23 |
| `p23-heirloom` | Describe something important that has been kept in your family for a long time | object-p23 |
| `p23-perfect-job` | Describe a perfect job you would like to have in the future | object-p23 |
| `p23-foreign-job` | Describe a short-term job you want to have in a foreign country | object-p23 |
| `p23-app` | Describe a program or app on your computer or phone | object-p23 |
| `p23-overspent` | Describe an item on which you spent more than expected | object-p23 |
| `p23-decision` | Describe an important decision that you made | event-p23 |
| `p23-early` | Describe a time when you got up early | event-p23 |
| `p23-group` | Describe a time when you worked in a group | event-p23 |
| `p23-sports` | Describe a live sports event you watched and liked | event-p23 |
| `p23-proud` | Describe a time when you felt proud of a family member | event-p23 |
| `p23-imagination` | Describe a time you needed to use your imagination | event-p23 |
| `p23-smiling` | Describe an occasion when many people were smiling | event-p23 |
| `p23-no-phone` | Describe an occasion when you were not allowed to use your mobile phone | event-p23 |
| `p23-advice` | Describe a time when you gave advice to others | event-p23 |
| `p23-bad-music` | Describe an event you attended in which you didn't enjoy the music played | event-p23 |
| `p23-encourage` | Describe a time when you encouraged someone to do something that he/she didn't want to do | event-p23 |
| `p23-vehicle` | Describe a bicycle/motorcycle/car trip you would like to go | event-p23 |

## Note C — Wave-population plan

When Wave 2-7 workers fill answers, they write to `topics[i].questions[j].answer_en` and `.answer_hint_zh` — never the structural fields. JSON shape stays stable.