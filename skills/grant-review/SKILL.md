---
name: grant-review
description: Review any research grant proposal top-down against what its panel scores — fit, then question, then layers, then reader sufficiency, then criteria coverage, then work plan, then prose — and stop at the highest level that is failing. Funder-independent; uses a funder guide and checker profile where one exists (BSF, ERC) and a criteria map built from the call otherwise. Includes guidance on what changes for smaller and collaborative grants. Use when asked to review, critique, strengthen or check a grant proposal or a section of one, for a funder without its own review skill, or when asked how to adapt a proposal from one funder to another.
---

# Reviewing a grant proposal, for any funder

You are reviewing a proposal that a few busy people will read once, looking for a reason to
rate it one grade lower. Find the highest-level thing that is wrong, and say what it costs
and to whom. The rules live in `references/` beside this file. Cite them by section so the
author can check you.

```
references/review_protocol.md   the ladder, the rubrics, the finding format.  Read §1–§4 first.
references/proposal_craft.md    the writing rules that travel between funders  (cite as craft §n)
references/grant_types.md       nine dimensions on which grant types differ, where schemes sit, advice per dimension
references/small_grants.md      what changes when the grant is small or collaborative (one corner of grant_types)
references/funder_profile.md    how to add a funder: a guide plus a checker profile
tools/grant_check.py            stages 8–9, any funder with a profile
tools/profiles/*.json           bsf, erc, generic
```

Read `review_protocol.md` §1–§4 before reporting. Read `proposal_craft.md` by section, as
findings need it, not end to end.

**Is there a funder skill?** If the call has its own skill, such as `bsf-review` beside this
one, or `erc-review` for ERC Starting and Consolidator grants, that skill is the entry point
and this one supplies its general layer. Otherwise work from this skill, and build the
criteria map yourself (protocol §1) from the call's documents. Ask the author for the call
text or reviewer form if you do not have it. Do not reconstruct criteria from memory. Then
place the call on the nine dimensions of `grant_types.md` (money, risk appetite, readers, grade
aggregation, right of reply, collaboration, career stage, documents, attempts) and read the
advice for each position before stage 1. Several large-grant habits invert at the small,
collaborative, expert-read end.

## Locating the tools

The draft is in the working directory, which is not this skill's directory:

```bash
GR=$(dirname "$(find ~/.claude -name grant_check.py -path '*grant-review*' 2>/dev/null | head -1)")
python3 "$GR/grant_check.py" --list-profiles
python3 "$GR/grant_check.py" --profile generic --census         # stage 0
python3 "$GR/grant_check.py" --profile generic proposal.docx    # stages 8-9
```

The checker reads `.tex`, `.md`, `.txt` and `.docx`, and reads `.pdf` when `pdftotext` is
installed. It maps files to proposal parts by filename and prints findings as
`file:line [code] message (rule)`, triaged BLOCK / SCORE / POLISH, followed by a list of
checks only a person can make. Name files explicitly when they do not follow the profile's
filename stems.

## Work top-down, and stop

| # | Stage | Question | Rubric |
|---|---|---|---|
| 0 | Census | What exists at all? | `--census` |
| 1 | Fit | May these people submit this, to this call, at this size? | protocol §4 stage 1 |
| 2 | Problem | A nameable question, with an instability and a cost? | protocol §4 stage 2; craft §2 |
| 3 | Layers | Each passage at its right altitude? | craft §3–§4 |
| 4 | Reader sufficiency | Can each reader score their criteria from what they see? | protocol §4 stage 4; craft §1 |
| 5 | Criteria coverage | Does every row of the criteria map have an address? | protocol §4 stage 5 |
| 6 | Work plan | Units, tasks, moonshots, risk, timeline, people and money | craft §9, §12 |
| 7 | Argument mechanics | Old before new, stress position, named causality, claim support | craft §10 |
| 8 | Prose | Fillers, hedges, voice, jargon | `grant_check.py` |
| 9 | Compliance | Format, limits, required headings and content, placeholders | `grant_check.py` |

**Report only from the highest stage with failures**, close with one line naming what you
deferred, and **report at most five findings**. Before writing anything, read the review
comments already in the draft. They are an open queue, and you should not re-raise them.

## What a finding looks like

1. **Where:** `file:line` and a short quote.
2. **What:** the defect, naming the rule (`craft §9.2`, `BSF §7`).
3. **Why it costs:** the criteria-map row and the reader. If you cannot name both, it is a
   preference. Drop it.
4. **What to do:** a concrete replacement in the author's register, or the missing content
   plus where it goes.

## Deciding what to do

- **Stages 1–7: do not edit.** Offer three routes per finding: *draft it*, *mark it* (a
  `\grscore{…}{…}` margin note in LaTeX, a native comment in Word), or *ask it*. Prefer
  *ask* whenever the fix needs a fact, result or intention you cannot see. The one stage-7
  carve-out you may fix directly is protocol §6.
- **Stages 8–9: just fix them** in the file, report a count, re-run the checker, and report
  before/after. Name each remaining flag that is a false positive.
- **At most three questions**, numbered, each answerable in one sentence.
- **Never invent** a citation, result, preliminary finding, or claim about an investigator
  or collaborator. **Never rewrite the argument silently.**

## Reporting

Drafts and comments go in the files. Chat carries the finding list, the reasons and the
questions, never a pasted rewritten section. Open with the stage reached and close with what
was deferred:

```
Stage 5 (criteria coverage) — 3 findings, reported below.
Deferred: stages 6–7 not run; checker: 2 BLOCK / 9 SCORE / 31 POLISH, unchanged.
By eye: suggested-reviewer conflicts not checked (no list in the folder).
```

## Moving a proposal between funders

When asked to adapt a proposal written for one funder to another, do not start from the
prose. Place both calls on the dimensions of `grant_types.md`, and build both criteria maps
(protocol §1) side by side. Each dimension where the two differ gives a list of edits. Typical moves: content that was parked in a second document must enter
the single plan; claims about feasibility switch from avoided to required; the vision shrinks
and the resources section grows (`small_grants.md` §3); a collaboration section appears with
named roles (`small_grants.md` §4); length moves between page-limited and word-limited
components. Report the list as findings against the *target* funder's criteria, then run the
ladder on the result.

## Emphasis

Deciding what a reader should carry away, and marking it, is a separate pass. That is the
`grant-writing` skill in `erc-review`. Run it after the review stages pass, not before,
because emphasising a section that fails stage 4 is wasted work.
