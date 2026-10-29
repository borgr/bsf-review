---
name: bsf-review
description: Review a U.S.–Israel Binational Science Foundation (BSF) Research Grant draft — regular or start-up — against what BSF referees and panels actually score, including cooperation as a separate gate, the "majority Excellent" funding threshold, the five required research-plan items, and the 12 pt / 1.5-spacing / 38-lines / 2 cm format rules. Works top-down and stops at the highest failing level. Also covers NSF-BSF and NEH-BSF submissions. Use when asked to review, plan, critique, check or improve a BSF proposal or any part of one (research plan, abstract, broader impacts statement, letters, budget justification, resubmission letter).
---

# Reviewing a BSF draft

A BSF proposal is read in full by three to five expert referees from several countries. A
binational panel then ranks it from their reviews. It is funded, typically, only when a
majority of referees rate it **Excellent**, a grade "reserved for near-perfect proposals where
there are few or no critical remarks", **and** it scores high on cooperation. So you are looking
for two things: the highest-level failure, and every plausible objection an expert could write
down. Either one costs the grant.

This skill is the BSF layer on top of `grant-review`, which sits beside it in this plugin:

```
references/BSF_writing_guide.md                  BSF rules, criteria, grade scale     (cite as BSF §n)
references/emphasis_overlay.md                   BSF notes for the grant-writing emphasis pass
../grant-review/references/review_protocol.md   the ladder, rubrics, finding format
../grant-review/references/proposal_craft.md    writing rules that travel            (cite as craft §n)
../grant-review/references/small_grants.md      what changes at small, collaborative funders
../grant-review/tools/grant_check.py            stages 8-9:  --profile bsf
```

**Read before reporting:** guide §6 (criteria map and grade scale) and §15 (the BSF deltas to the
ladder), then `review_protocol.md` §3–§5. Read everything else by section as findings need it.

**Is this really a BSF review?** If the proposal is an **NSF-BSF** or **NEH-BSF** submission,
NSF or NEH scores it under their criteria and the BSF does not evaluate merit (guide §13). Say
so in one line, use `grant-review` with the NSF solicitation as the criteria source, and apply
only guide §13 from this skill.

**Check the guide is current.** Guide §14 names the regulations and the date checked (the 2026
cycle). The BSF reissues its regulations every year. If the draft targets a later cycle, say so
at the top of the report and treat the guide's numbers as claims to re-verify.

## Locating the checker

```bash
GR=$(dirname "$(find ~/.claude -name grant_check.py -path '*grant-review*' 2>/dev/null | head -1)")
python3 "$GR/grant_check.py" --profile bsf --census          # stage 0
python3 "$GR/grant_check.py" --profile bsf                   # stages 8-9, all parts in the cwd
python3 "$GR/grant_check.py" --profile bsf --pages           # + page counts
python3 "$GR/grant_check.py" --profile bsf --json            # for parsing
```

It recognises `research_plan`, `abstract`, `broader_impacts`, `references`,
`resubmission_letter`, `progress_report`, `lay_abstract` and `publications` by filename, in
`.tex`, `.md`, `.txt` or `.docx`. It reads font, spacing and margins from the source, and
estimates lines per page for LaTeX. **LaTeX's `\onehalfspacing` at 12 pt on A4 with 2 cm margins
sets about 40 lines, which breaks the 38-line cap** (guide §3). It ends with a by-eye list. Report
those items alongside the machine findings, because no script can see them.

## Work top-down, and stop

Use the ten stages of `review_protocol.md` §3 with the deltas in guide §15. In short:

| # | Stage | BSF emphasis |
|---|---|---|
| 0 | Census | which parts exist; is the plan at 15 pages? |
| 1 | Fit | area open this year; eligibility and one-at-a-time rules; submissions left; **one programme by two groups in both countries**, sized to the award this kind of project **actually receives** (theory ~$150–200k, lab ~$200–300k; guide §9) |
| 2 | Problem | nameable question, **stated hypotheses** ("Fair" = no clear question or hypotheses); **page-1 test** (guide §4.1): question, hypothesis, objectives, why two groups |
| 3 | Layers | as general; two or three objectives, four at most, interdependent across the groups but not blocking in sequence (guide §4.4) |
| 4 | Reader sufficiency | **expert test** (each half's referee finds nothing hand-waved), **adviser test** (abstract + page 1 are the summary you want given), and **origin test** (four in five referees are not Israeli) |
| 5 | Criteria coverage | **A** merit, **B** importance, **C** cooperation (the seven tests of guide §7), **D** PIs and environment, **E** schedule, **R** previous BSF record, **X** five required items. **Feasibility is scored here — demonstrate it.** Run the **objection audit** (guide §4.11) and check for **quotable strengths** (guide §6) |
| 6 | Work plan | one block per objective with its five parts: hypothesis, evidence, tasks, success criterion, if-then pitfalls (guide §4.6); a lead group per task; schedule form agrees with item 3; people ↔ budget; visits in the timeline |
| 7 | Mechanics | **name the acting group**; "we will" runs hide the collaboration |
| 8 | Prose | English quality is on the grade scale |
| 9 | Compliance | `grant_check.py --profile bsf`, plus the by-eye list |

Report only from the highest failing stage, with **at most five findings**, and close with
one line naming what was deferred. Before writing anything, read the review comments already in
the draft.

## What a finding looks like

1. **Where:** `research_plan.tex:112` or `research_plan.docx ¶41`, plus a short quote.
2. **What:** the defect, naming the rule (`BSF §7`, `craft §9.2`).
3. **Why it costs:** the criterion (A–E, R, X) and the reader: *"a U.S. referee in
   computational modelling has no way to tell what the Israeli group contributes to WP2. That is
   question C(a), and a weak C blocks funding even with Excellent merit (BSF §6)."* If you
   cannot name both, drop the finding.
4. **What to do:** a concrete replacement, or the missing content and where it goes. When the
   fix needs to know who does what, which result exists, or what a partner will provide, the
   output is a **question**.

## Deciding what to do

- **Stages 1–7: do not edit.** Per finding, offer *draft it*, *mark it*, or *ask it*. To mark
  it, use `\grscore{BSF 7}{…}` with `grantreview.sty` in LaTeX, or a native Word comment
  `SCORE · BSF 7 — …`. Prefer *ask* for anything about roles, preliminary results, equipment,
  other funding or previous joint output. Those are facts about two groups that you cannot see,
  and inventing them is the worst error available here.
- **Stages 8–9: fix directly**, re-run the checker, and report before/after counts and any
  false positives by name.
- **At most three questions**, numbered, one sentence each.
- **Never invent** a role, result, citation, collaboration history or resource. **Never rewrite
  the argument silently.**

## Other jobs this skill does

- **Planning a plan.** Use guide §4: the item headings and page split, then §4.1–§4.10 for what
  each section must contain, and the element map in §4.12 as the checklist. Start from the
  annotated skeleton in `templates/bsf/` (`research_plan.tex`, `.md` or `.docx`); every `[[slot]]`
  left unfilled is reported by the checker. Hand back the outline in the three levels of
  `review_protocol.md` §9: a causal one-sentence chain, one claim per paragraph, then slots. Mark
  which group owns each slot. For a field where "hypothesis" fits badly (mathematics, empirical
  computer science, the social sciences), translate each element with `proposal_craft.md` §14
  rather than dropping it.
- **Abstract, broader impacts, lay abstract.** Guide §8. Check each against its own reader and
  word limit, and check that the Broader Impacts Statement is not an NSF section pasted in.
- **Letters of collaboration.** Guide §7, §10. Each letter names its writer's tasks, facilities
  and visits, in the writer's voice. A letter that only confirms participation is a finding
  against criterion C.
- **Resubmission.** Guide §11 first: is this submission allowed, and is the area change
  approved? Then the **resubmit-or-reframe gate**. Sort the previous weaknesses into fixable
  and fatal, and say which this is before drafting anything. Then review the letter against
  the previous reviews **and the panel summary**, using the seven-part structure in guide §11,
  and check that every change it claims is in the plan. Finally run the ladder on the changed
  sections (`review_protocol.md` §7, `resubmission` scope). The checker flags a missing summary
  of changes, an unaddressed panel, unlocated changes and defensive phrasing.
- **Start-up.** Guide §12: a feasibility argument in place of preliminary data, an exit
  statement, the senior partner in the work plan, the ideas visibly the junior's, and scope for
  $90k over two years. The bar is Excellent *or* Very Good, but the criteria are the same.
- **Choosing suggested reviewers.** Guide §10. About two of your four or five referees come from
  this list. Check every conflict rule, and check that the names cover both halves of the
  project.
- **Budget justification.** Guide §9. Cap, overhead, the no-PI-salary rule, the 20 % equipment
  cap, the visit rules and joint-only publication charges. Check that every budgeted person
  appears in a task.
- **Moving a proposal to the BSF from another funder** (ERC, ISF, NSF): follow
  `grant-review/SKILL.md` *Moving a proposal between funders*. From an ISF plan, read guide §4.13
  first, including the ISF overlap rule. The usual list is to add
  hypotheses and fallbacks, shrink the vision, add a collaboration section with named roles,
  grow item 5, and restructure under the five required items.

## Reporting

```
Stage 5 (criteria coverage) — 3 findings: C ×2, A ×1. Reported below.
Deferred: stages 6–7 not run; checker 1 BLOCK (lines-per-page) / 6 SCORE / 22 POLISH, unchanged.
By eye: suggested reviewers not in the folder — not checked.
```

Drafts and comments go in the files. Chat carries findings, reasons and questions.

## Emphasis

After the ladder passes, the emphasis pass is `grant-writing` in `erc-review`. Its corpus is ERC
and NIH, so read `references/emphasis_overlay.md` here first. It says which device readings
transfer to a single-document, expert-read, majority-Excellent scheme, and which invert.
