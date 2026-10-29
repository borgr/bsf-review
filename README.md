# bsf-review

A kit for writing and reviewing grant proposals, in two layers. The **general layer** is a
review protocol that works top-down for any funder, the writing rules that hold at every panel,
a guide to what changes when the grant is small or collaborative, and a checker driven by
funder profiles. The **BSF layer** applies all of that to the U.S.–Israel Binational Science
Foundation, whose referees, panels and grade scale are documented closely enough to write to
directly.

It is the sibling of [erc-review](https://github.com/borgr/erc-review), which does the same
for ERC Starting and Consolidator Grants. The general layer here was extracted from it. Rules
that held for every funder were kept and generalised, and everything ERC-specific was left
behind.

## Why the BSF needs its own layer

The same science, written the same way, scores differently at the BSF than at a large scheme.
Four reasons, each of which inverts an ERC habit:

- **Every page is read by an expert.** Three to five referees read the full plan, and there
  is no generalist stage.
- **The funding threshold is "Excellent from a majority"**, and Excellent is "reserved for
  near-perfect proposals where there are few or no critical remarks". One plausible objection
  costs the grant, so fallbacks and demonstrated feasibility are scored rather than avoided.
- **Cooperation is a separate gate.** Excellent science by one lab with a partner's name
  attached is not funded.
- **The money is small.** The cap is $300,000 across two groups over four years, and typical
  awards are lower: a median of about $190,000 in computer science and maths, and $284,000 in
  the life sciences. Ambition is judged against what the grant buys, and the resources section
  carries the part of the project the grant does not pay for.
- **Your referee list matters.** About two of the 4–5 referees come from the six names you
  suggest, and one panel adviser summarises the reviews for the panel.

## What is here

| | |
|---|---|
| [`skills/grant-review/SKILL.md`](skills/grant-review/SKILL.md) | Reviews any funder's proposal against a criteria map built from the call. Ten stages, reports from the highest one failing. |
| [`…/references/review_protocol.md`](skills/grant-review/references/review_protocol.md) | The ladder, the stage rubrics, the finding format, scoping, margin comments, outlines. |
| [`…/references/proposal_craft.md`](skills/grant-review/references/proposal_craft.md) | Writing rules that travel between funders, each with a **Varies:** line where a funder changes its force. §14 is the element catalogue: what reviewers expect in any research plan, and what each element looks like in the experimental sciences, mathematics, empirical computer science and the social sciences. |
| [`…/references/grant_types.md`](skills/grant-review/references/grant_types.md) | Nine dimensions on which grant types differ (money, risk appetite, readers, grade aggregation, right of reply, collaboration, career stage, documents, attempts), where BSF, ERC, NSF, NIH, ISF, SNSF and HFSP sit, and evidence-backed tests per dimension. |
| [`…/references/small_grants.md`](skills/grant-review/references/small_grants.md) | What changes at small, collaborative and early-career funders: readers, grade aggregation, ambition, collaboration, short documents, resubmission. |
| [`…/references/funder_profile.md`](skills/grant-review/references/funder_profile.md) | How to add a funder: a guide plus a checker profile, no code. |
| [`…/tools/grant_check.py`](skills/grant-review/tools/grant_check.py) | Settles everything a regex can, for any funder with a profile. `.tex`, `.md`, `.txt`, `.docx`, and `.pdf` with `pdftotext`. Standard library only. |
| [`…/tools/profiles/`](skills/grant-review/tools/profiles/) | `bsf`, `erc` (a demonstration), `generic`. |
| [`skills/bsf-review/SKILL.md`](skills/bsf-review/SKILL.md) | The BSF entry point: regular and start-up grants, and NSF-BSF routing. |
| [`…/references/BSF_writing_guide.md`](skills/bsf-review/references/BSF_writing_guide.md) | The BSF rules, criteria verbatim, the grade scale, the collaboration, budget, resubmission, start-up, NSF-BSF, and the review overlay (§15). §4 goes section by section through the research plan, with page budgets, what referees look for, failures and examples, and maps every expected element to where it lives (§4.12). |
| [`…/references/emphasis_overlay.md`](skills/bsf-review/references/emphasis_overlay.md) | A `# BSF` section for erc-review's `grant-writing` emphasis pass. Unmeasured, and says so. |
| [`grantreview.sty`](grantreview.sty) | Margin-note macros keyed to rules: `\grblock`, `\grscore`, `\grpolish`. |
| [`templates/bsf/`](templates/bsf/) | An annotated research-plan skeleton in LaTeX, Markdown and Word, every element a `[[slot]]` with its rule. Format-compliant; the checker reports each unfilled slot. |
| [`example/`](example/) | A deliberately flawed BSF draft. |
| [`evals/`](evals/) | Four scenarios, plus unit tests for the checker. |

## Using the checker

No dependencies beyond Python 3.9+. Run it from the folder holding the proposal parts. It
recognises them by filename (`research_plan.*`, `abstract.*`, `broader_impacts.*`, …), or you
can name the files.

```sh
GR=path/to/bsf-review/skills/grant-review/tools
python3 $GR/grant_check.py --profile bsf --census     # stage 0: what exists
python3 $GR/grant_check.py --profile bsf              # everything, triaged BLOCK/SCORE/POLISH
python3 $GR/grant_check.py --profile bsf --pages      # + page counts (.docx: Word's count; .tex: needs tectonic)
python3 $GR/grant_check.py --profile bsf --json       # for an agent
python3 $GR/grant_check.py --profile generic my_nsf_project_description.docx
```

Try it on the example first: `python3 skills/grant-review/tools/grant_check.py --profile bsf example/`.
To start a plan, copy `templates/bsf/research_plan.tex`, `.md` or `.docx` and fill the slots.

Beyond format and required items, the BSF profile looks for a trace of each element referees
expect (guide §4.12): a hypothesis and objectives on the first page, preliminary results, a
timeline, a reason for the pairing, exchange visits, and, inside every objective block, a
success criterion and pitfalls. It also counts objectives and checks that item 3 outweighs
items 1 and 2. These are presence checks: they find a missing element, not a weak one.

Findings print as `file:line [code] message (rule)`. A rule is `craft §n` for the general
rules and `BSF §n` for the funder's, so a margin comment can cite the rule rather than an
opinion. Each run ends with a **by-eye** list of what no script can check, such as
reviewer-list conflicts, signed letters, budget arithmetic in the online form and the
grants-office deadline.

One check is worth knowing about before you format anything. **LaTeX's `\onehalfspacing` is
not 1.5× line spacing.** At 12 pt on A4 with 2 cm margins it sets about 40 lines per page,
over the BSF's 38-line cap. `\linespread{1.5}` gives about 34. The checker estimates this from
the source.

## Using the skills

```sh
claude plugin marketplace add borgr/bsf-review
claude plugin install bsf-review@bsf-review
```

Ask for a review of a BSF draft and `bsf-review` runs. Ask about any other funder and
`grant-review` runs, building the criteria map from the call text you give it. Ask to move a
proposal from one funder to another and `grant-review` lists what moves before touching prose.

For the emphasis pass, install `erc-review` too. Its `grant-writing` skill is
funder-independent, and `bsf-review`'s `emphasis_overlay.md` supplies the BSF readings.

## Adding a funder

Write a guide in the shape of `BSF_writing_guide.md` and a JSON profile in the shape of
`profiles/bsf.json`. `funder_profile.md` lists every field and the order of authority for
sources. ISF, GIF, NSF directorates and national councils fit the pattern. Contributions
welcome.

## Caveats

**Verified on 28 October 2026 against the BSF 2026 cycle.** The sources are the
*Regulations for Online Submission* (updated August 2026), the *Guidelines for Reviewers*,
the BSF's evaluation, statistics and FAQ pages, and the NSF-BSF CISE call. Guide §14 lists
them and the things that are easy to get wrong from older advice. The BSF reissues its
regulations every year, and the version for **your** cycle is the authority.

**The general layer is an editorial position.** It holds that fixing framing before prose is
strictly better, that a finding without a named criterion and reader is a preference, and
that small grants are lost by their most plausible objection. These are arguments from the
documented review processes, not funder policy.

**What is measured, and what is not.** No BSF research plan is public, so nothing about plan
structure is measured from BSF plans. Guide §16 measures what is public: award sizes, team
sizes and titles of 513 regular grants from the BSF's database, the lay abstracts that funded
applicants wrote, and 83 NSF-BSF award abstracts. The section shares and critique patterns in
guide §4 and `grant_types.md` come from funded NIH and NSF analogues with public reviews. They
are labelled as analogues. The emphasis numbers in `erc-review` come from funded ERC and NIH
documents, and the BSF emphasis overlay is marked as direction, not rate.

**No real proposals.** Every example and fixture is invented.

## Licence

Code (`skills/*/tools/`, `grantreview.sty`, `example/`, `templates/`, `evals/fixtures/`): MIT. Prose
(`SKILL.md` files, `references/`, evals, this README): CC BY 4.0. See [LICENSE](LICENSE).

---
More tools and guides by Leshem Choshen: [tools](https://borgr.github.io/tools/) · [guides](https://borgr.github.io/guides/) · [homepage](https://borgr.github.io/)
