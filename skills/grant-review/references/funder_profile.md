# Adding a funder

A new funder costs two files and no code: a **guide** that says what the call wants, and a
**checker profile** that says what a script can settle. `bsf-review` is the worked example
of both. Build them from the funder's own documents, in this order of authority:

1. **The reviewer guidelines or reviewer form.** This is what the reader holds while scoring,
   so it outranks the applicant instructions on what is scored and how grades combine.
2. **The call or regulations for this year.** These are the authority on eligibility, limits,
   format, required content and budget. Note the version and date, because many funders
   reissue them every year and the changes are where old advice goes wrong.
3. **The funder's FAQ and evaluation pages.** These often state the policy behind a rule,
   such as "the grant is mostly given to support the cooperation", which the regulations
   leave implicit.
4. **Grants-office and practitioner material.** Useful for habits and traps. Label it as
   practice, never as rule, and let the funder's documents win any disagreement.

## The guide

Number the sections and keep the numbers stable, because the checker profile, the review
skill and the margin comments cite them. Most funder guides need these sections. Skip any
that the call does not have.

| Section | Must answer |
|---|---|
| What the funder funds and rejects | the shapes that get desk-rejected, in the funder's words |
| Call mechanics | dates, eligibility, concurrency limits, resubmission rules, fields open this cycle |
| What you submit | every component, its limit, its format rules, and who sees it |
| Required content | anything whose absence is non-compliance, verbatim |
| Who reads what | the reader table from `proposal_craft.md` §1, filled in |
| Evaluation criteria | **verbatim**, with shorthands: this is the criteria map of `review_protocol.md` §1 |
| How grades combine | the grade scale and the funding threshold, verbatim where published |
| Funder-specific writing advice | only what does not already hold everywhere; cite `craft §n` for the rest |
| Budget | caps, overhead, eligible and ineligible costs |
| What this was checked against | each source, its version, the date you checked, and what changed recently |
| Review overlay | the stage-by-stage deltas to `review_protocol.md`: items to add, and general items whose force changes here |

The last section is what makes the guide usable by the review skill. Write it as differences
only. For example, at the BSF the feasibility item flips from "do not assert it" to "it is
scored, demonstrate it", and stage 5 gains a cooperation item. Do not copy the general
rubric.

**Separate measured from advised.** "Typically only proposals rated Excellent by a majority
are funded" is the funder's own statement. "Name the site for every task" is advice derived
from it. Keep the two distinguishable, so that a later reader knows which one to re-verify.

## The checker profile

A JSON file in `tools/profiles/`. Every field is optional except `name`, `guide` and `parts`.

```json
{
  "name": "Funder Programme 2027",
  "guide": "FUND",
  "verified": "YYYY-MM-DD, against <documents and versions>",
  "main_part": "research_plan",
  "parts": {
    "research_plan": {
      "stems": ["research_plan", "plan"],
      "page_limit": 15,
      "word_limit": null,
      "word_limit_severity": "BLOCK",
      "char_limit": null,
      "word_floor": null,
      "required": true,
      "rule": "FUND §3",
      "required_heading": "Research Plan",
      "format": {"min_font_pt": 12, "min_line_spacing": 1.5, "min_margin_cm": 2.0,
                 "max_lines_per_page": 38, "rule": "FUND §3"},
      "required_content": [
        {"code": "item3-roles", "any": ["regex", "regex"], "severity": "BLOCK",
         "message": "what is missing, in the call's words", "rule": "FUND §4"},
        {"code": "opening-hypothesis", "within_words": 450, "any": ["hypothes"],
         "severity": "SCORE", "message": "...", "rule": "FUND §4.1"}
      ],
      "unit_requirements": [
        {"code": "objective-success", "title": "^(?:[\\d.]+\\s*)?Objective\\s*\\d",
         "min_words": 120, "any": ["success", "criteri"], "severity": "SCORE",
         "message": "...", "rule": "FUND §4.6"}
      ],
      "max_objectives": {"pattern": "\\bObjective\\s*([1-9])\\b", "max": 4,
                         "severity": "SCORE", "message": "...", "rule": "FUND §4.4"},
      "proportions": [
        {"code": "methods-share", "a": "method", "b": "background|objective", "ratio": 1.0,
         "severity": "SCORE", "message": "...", "rule": "FUND §4"}
      ]
    }
  },
  "patterns": [
    {"code": "pi-salary", "pattern": "regex", "flags": "i", "severity": "BLOCK",
     "message": "\"{match}\" -- why it costs", "rule": "FUND §9",
     "parts": ["research_plan"], "body_only": true, "once": false}
  ],
  "disable": ["passive"],
  "manual_checks": ["what no script can check, with its rule"]
}
```

Notes on the fields that are easy to get wrong:

- **`stems`** map files to parts by filename: `research_plan.docx`, `my_research_plan.tex`
  and `research_plan_v3.md` all match `research_plan`. An editable source wins over a PDF of
  the same stem.
- **`required_content`** is the cheapest high-value check, because absence of required
  content is the most common reason for return without review. Each item passes if *any* of
  its patterns appears anywhere in the body. Keep patterns broad. The check exists to catch
  a section that was never written, not to judge one that was.
- **`within_words`** on a `required_content` item confines the search to the opening N words,
  for what must be on the first page, and **`until_heading`** stops it earlier at the first
  heading matching a pattern, such as item 1. **`headings_only`** accepts a match only in a
  heading, for "give it its own section" rules, where the word in running text proves nothing.
- **`item_headings`** is a pattern naming the funder's items. The structure rules below work at
  the shallowest heading level where at least two headings match it, so a plan whose items are
  `\subsection`s under a numbered `\section{Research Plan}` is read correctly.
- **`unit_requirements`** apply to every heading whose title matches `title`, and search the
  text under it, nested headings included. `min_words` skips one-line mentions, such as an
  objective named in a list. `within` confines the rule to blocks under a matching item, so that
  objectives restated in item 2 are not asked for item 3's success criteria. Use them for what
  each block of a repeated structure must hold. Structure is read from `.tex`, `.md` and `.docx`
  headings (Word's Heading styles), not from PDF.
- **`max_objectives`** counts the distinct numbers captured by `pattern`, anywhere in the file.
- **`proportions`** compare the item-level sections whose titles match `a` with those matching
  `b`, and flag when `a` has fewer than `ratio` times the words of `b`. When either side has no
  matching heading, a POLISH `<code>-unknown` says the check did not run.
- **`word_limit_severity`**: use `SCORE` where the call says "about N words", and `BLOCK` where
  it says "N words or less is required".
- **`format`**: font, spacing and margins are read from `.tex` and `.docx` sources. Lines per
  page is estimated for `.tex` from the class, the spacing command and the geometry, and is
  worth having because LaTeX's `\onehalfspacing` is not 1.5× and can break a lines-per-page cap
  (`bsf-review` §3).
- **`task_owner`** (`{"any": [regex, ...], "severity", "rule"}`) flags every heading named as a
  task ("Task 2.1", "T3", a moonshot) whose text matches none of the patterns, for funders that
  score who does what. Name groups, sites or roles; generic nouns such as "the team" prove nothing.
- **`patterns`** with `"scope": "paragraph"` match across source lines joined into paragraphs,
  for runs such as three "We will" sentences that a line-by-line match would miss.
- **`patterns`** cite the funder guide, never `craft`. A rule that holds for every funder
  belongs in `grant_check.py`'s built-in list instead.
- **`disable`** turns off a built-in rule where this funder's readers want the opposite.
  Use it sparingly, and say why in the guide.
- **`manual_checks`** are printed at the end of every run. Put there everything that costs
  the proposal and that no script can see: reviewer-list conflicts, signed letters, budget
  arithmetic in an online form, the institution's internal deadline.

Then test the profile against a deliberately flawed fixture, as `example/` does for the
BSF. A profile that has never produced a finding has not been tested.
