# Review protocol, for any funder

A rubric worked from the top down, not a checklist worked through. Fixing an early stage
rewrites everything downstream of it, so findings below an open failure are wasted work. A
draft whose question is not nameable gains nothing from twenty notes on passive voice. It
needs one note about the question, and silence about the rest until that is settled.

This is the funder-independent form of §13 of the ERC guide in `erc-review`. The ladder is the
same, but the stages that named ERC readers and questions now take them from a **criteria
map** that you build for the call in hand (§1). A funder guide such as
`bsf-review/references/BSF_writing_guide.md` supplies that map, and also supplies the
rubric items that hold only for that funder.

## 1. Before anything: the criteria map

A finding is actionable only when it names what it costs: which scored question, read by
which reader. So before the first stage, write the funder's evaluation criteria down
**verbatim**, give each a shorthand, and record who scores it from which documents:

| Shorthand | Criterion, verbatim from the call | Scored by | From which documents | Weight or aggregation |
|---|---|---|---|---|
| C1 | … | … | … | … |

Take the wording from the funder's current call and reviewer guidelines, not from memory or
a colleague's notes. The reviewer guidelines are the better source where both exist,
because they are what the reader actually holds. Then add one row per **unscored but
enforced** requirement: compliance items and required content whose absence gets a proposal
returned without review. These are BLOCK-severity rows.

Two standing rules come with the map.

- **Anything you cannot point to a location for is missing, not implicit.** "It is implied by
  the objectives" is how proposals lose the criterion they thought they had covered.
- **A finding that cannot name a row is a preference.** Drop it, or say plainly that it is
  taste.

## 2. Severities

| Severity | Meaning | Consequence if left |
|---|---|---|
| **BLOCK** | Compliance breach, missing required content, or unwritten placeholder | Not submittable, or returned without review |
| **SCORE** | Weakens the answer to a named criterion | Costs grade from a named reader |
| **POLISH** | Sentence-level | Costs goodwill, not grade |

The checker (`tools/grant_check.py`) and the comment macros (`grantreview.sty`) use the
same three words.

## 3. The stage ladder

| # | Stage | The question the stage asks | Reported as |
|---|---|---|---|
| 0 | **Census** | What exists at all? | not reported — a map |
| 1 | **Fit** | May these people submit this, to this call, and is it the kind of project the call funds? | BLOCK on the framing |
| 2 | **Problem** | Is there a nameable question, with an instability and a cost? | SCORE on the significance criterion |
| 3 | **Layers** | Is each passage at its right altitude? | SCORE on significance/approach |
| 4 | **Reader sufficiency** | Can every reader score their criteria from the documents they actually see? | SCORE, per reader |
| 5 | **Criteria coverage** | Does every row of the criteria map have an address? | SCORE or BLOCK, per row |
| 6 | **Work plan** | Are work units and tasks correctly typed, bounded, staffed, and scheduled? | SCORE on approach/feasibility |
| 7 | **Argument mechanics** | Do the sentences carry the argument's joints? | SCORE or POLISH |
| 8 | **Prose** | Fillers, hedges, voice, jargon, tics | POLISH, machine-checked |
| 9 | **Compliance** | Format, length, required headings, placeholders, citations | BLOCK, machine-checked |

**Report only from the highest stage with failures.** Close with one line naming what you
deferred and at which stage, so the author knows the review is unfinished rather than clean.

**At most five findings per report.** More than that is a rewrite the author cannot review.
If a stage has more, report the five with the largest consequence and say how many remain.

Stage 0 first, always: `grant_check.py --profile <funder> --census`. It reports words per
part, unwritten units, placeholders, and length against the limit, which is enough to know
which stages can be answered. A part sitting **at** its limit changes every later stage,
because from then on each suggestion must name what it displaces.

## 4. Stage rubrics

Each item gives a **test**, the **cost** if it fails (stated as a criteria-map row and a
reader), and what to **suggest**. Rules cite `craft §n`, which is `proposal_craft.md` beside
this file.

### Stage 1 — Fit

- **The applicants may submit this.** *Test:* the funder's eligibility, collaboration and
  resubmission rules against the applicants' situation. That covers career-stage windows,
  concurrent-grant limits, how many times this proposal has been submitted, and whether the
  field is open this cycle. *Cost:* the whole application, because these are checked before
  any reviewer reads a word. *Suggest:* settle it with the grants office in the first
  conversation; if a bar applies, the question becomes which call, and the draft is not
  wasted.
- **The project is the shape this call funds.** *Test:* the funder guide's description of what
  it funds and what it rejects, against the aim. Typical mismatches are a programme presented
  as a project, a service or tool where the call wants a question, a single-lab project
  presented as a collaboration, or a step-change pitch on a budget that buys a paper or two
  (`small_grants.md` §3). *Cost:* the significance criterion, and often desk rejection.
  *Suggest:* change the aim or the call, not the paragraph.
- **The scope fits the money, the people and the time.** *Test:* count objectives and the
  methods each needs against the budget, the named staff and the duration. *Cost:* the
  feasibility or timeline criterion, and also significance, because over-scoping reads as
  not understanding the work. *Suggest:* cut an objective rather than thinning all of them.

### Stage 2 — Problem

- **The question is nameable** (craft §2.1). *Test:* page 1; passes when a reader outside the
  subfield can write the question in one sentence after one reading, unprompted. *Cost:* the
  significance criterion, from every reader. *Suggest:* move the question to the first
  paragraph and cut what is there now.
- **The opening is a problem, not a topic** (craft §2.4). *Test:* the first paragraph
  contains an instability and a cost to these readers. *Suggest:* find the "but" hidden behind
  an "and"; name an error before a gap.
- **Limitations and barriers both present** (craft §2.2). *Test:* one sentence says what is
  unknown and a different one says why. *Suggest:* ask what blocked prior attempts, since the
  answer is usually also the why-now.
- **The challenge is falsifiable** (craft §2.3, machine-flagged). *Suggest:* replace with the
  specific claim that would have to be wrong.

### Stage 3 — Layers

- **Vision and aim separate** (craft §3). *Test:* the vision outlives the grant and the aim
  completes inside it.
- **3–5 objectives, each a knowledge claim, dependencies stated** (craft §4,
  machine-flagged for deliverable verbs).
- **Every passage at one level** (craft §3). *Test:* no objective-level section describes a
  task, and no work unit floats free of an objective. *Suggest:* move material rather than
  rewrite it, because misplaced material is usually good material.

### Stage 4 — Reader sufficiency

The generalisation of the ERC's "Step-1 sufficiency". Take each row of the reader table
(craft §1) and close every document that reader does not see.

- **Each reader can score their criteria from what they see.** *Test:* for an eliminating
  stage that sees a subset of the documents, check that the subset alone answers every
  criterion that stage scores. For a single document read by experts, check that the first
  two pages alone answer significance, because the panel member who presents a proposal
  from three reviews often has only that much of it in mind. *Cost:* the criteria that reader
  scores, silently. *Suggest:* name what to lift and what it displaces.
- **Written for the reader who actually reads it.** *Test:* for generalists, every term not
  universal outside the subfield is defined or gone. For expert referees, no step is
  hand-waved that an expert would want to see. *Cost:* significance (generalists) or approach
  (experts).
- **Headings answer the criteria.** *Test:* the table of contents; passes when a reviewer
  scoring criterion N finds its section without searching. *Suggest:* make headings answer
  rather than label.

### Stage 5 — Criteria coverage

One row of the criteria map at a time: find its address. Recurring failures that hold across
funders:

- **Timeliness argued, not asserted** (craft §7).
- **Team fit shown, not claimed** (craft §7, §11). *Suggest:* replace the claim with the
  evidence that produced it.
- **Impact has a *because*** (craft §8), and, where the funder scores broader or societal
  impact separately, that row has its own address in the funder's own sense of the word.
- **Feasibility handled the way this funder's readers score it.** Where an eliminating
  stage does not score feasibility, asserting it there spends space on an unscored claim,
  which is the ERC Step-1 case. Where referees score it, which is most single-document
  funders, it must be demonstrated through specificity, preliminary data and fallbacks. It is
  never shown by the word "feasible". **Check the funder guide before reporting either
  way.**
- **Every BLOCK row present.** Required sections, statements, letters and forms.

### Stage 6 — Work plan

- **Every work unit has a one-sentence outcome objective and a 2–5-sentence rationale**
  (craft §9.2). *Suggest:* they are usually both present and both labelled "objective";
  relabel one.
- **Objectives map visibly to work units** (craft §9.1).
- **Tasks read purpose → approach → contribution, as prose, with who, the check and the
  fallback** (craft §9.3; length machine-flagged).
- **Each moonshot bounded and informative either way** (craft §9.4).
- **Risk answers why take this risk; conceptual risk is a paragraph** (craft §9.5).
- **Timeline shows decision points, and agrees with any schedule form** (craft §9.6).
- **People and money agree with the plan** (craft §12). Every named person appears in the
  budget or is said to be paid for elsewhere. In a collaborative grant, every task names which
  site does it.

### Stage 7 — Argument mechanics

- **Old information before new.** Read the first six words of each sentence. When a sentence
  has nothing to stand on and cannot be repaired without inventing a connection, you have
  found a hole in the *argument*. Report it as a question, not a transition.
- **A repeated opener marks a set or nothing** (craft §10). Do not fix by quota.
- **The stress position carries the payload.**
- **Causal chains named** (craft §10, machine-flagged).
- **Every claim cited, shown, or softened**, including subordinate clauses.

### Stages 8 and 9 — machine-checked

Do not spend reasoning on these. `grant_check.py` settles them, cites the rule, and triages by
severity. Fix them directly in the file and report a count. Then re-run and report
before/after numbers. Name each remaining flag that is a false positive, such as a passive
with no human agent or a filler word inside a quoted title, rather than leaving it silently.

## 5. What a finding looks like

1. **Where:** `file:line`, plus a quote short enough to locate the sentence.
2. **What:** the defect in one sentence, naming the rule (`craft §9.2`, or the funder guide's
   section).
3. **Why it costs:** the criteria-map row and the reader. If you cannot name both, drop it.
4. **What to do:** a concrete replacement in the author's register, or the specific missing
   content plus where it goes. "Tighten this" is not a suggestion.

## 6. Deciding what to do

**Stages 1–7 — do not edit.** Report and offer three routes per finding: **draft it** (you
write the replacement, the author reviews the diff), **mark it** (a margin comment at the
site), or **ask it** (the fix needs a fact only the authors have). Prefer *ask* whenever the
fix needs a fact, result, or intention you cannot see.

**One carve-out inside stage 7 — just fix these:** a definite reference with no antecedent, a
missing link at a seam, a tangled preposition, a word repeated where a second word is meant.
Report the count. The line is whether the claim, its ground and its consequence still stand in
the same relation afterwards.

**Stages 8–9 — just fix them**, and report a count.

**Batch questions.** At most three, numbered, each answerable in one sentence, and only those
that block the next edit. Everything else goes into the draft as comments.

**Two hard constraints.** Never invent content, whether a citation, a result, a preliminary
finding, or a claim about an investigator or a collaborator. When a fix needs knowledge that
is not in the draft, the output is a question. Never rewrite the argument silently.

## 7. Scoping a review

| Invocation | Scope | Stages |
|---|---|---|
| full review | every part | ladder from 0; stop at the first failing stage |
| `skim` | headings and first sentences only | 2–4, cheaply |
| one part or section | that part | the stages it can answer |
| one work unit | that unit | 6 |
| `cut N` | a part over its limit | 9, reporting what was sacrificed |
| `resubmission` | the letter plus the changed sections | 5 against the previous reviews, then the ladder |

**Skim** is worth its own mention. If the argument does not survive reading only headings
and first sentences, the openings or the order are wrong, and no amount of body-text editing
will fix it.

## 8. Leaving a finding in the draft

Chat carries the finding list and the questions. The draft carries what must survive the
conversation.

**LaTeX:** `grantreview.sty` takes a rule reference plus the comment:

```latex
\grblock{BSF 4}{research plan item 3 never names the U.S. PI's role}
\grscore{craft 9.2}{this is the rationale, not the objective}
\grpolish{craft 10}{"and then" hides the causal step}
\listofgrcomments
```

`\usepackage[off]{grantreview}` drops them all for the submission build.

**Word or Google Docs:** use the native comment, opening with the severity and rule:
`SCORE · craft 9.2 — this is the rationale, not the objective`. Do not type review notes
into the body text of a document that will be uploaded as-is.

Four conventions apply in both formats: put the severity in the marker, not the prose; say
where the missing thing goes; read the existing comments before adding any, because they are
an open queue; and when the fix needs a fact you do not have, ask rather than draft.

## 9. Handing back an outline

Planning a section is a different job from reviewing one, and an outline the author cannot read
is worse than none. Give three levels, always in this order, and never only one of them.

1. **The section in one sentence, as a causal chain.** "A holds, so B is testable, which changes
   C, so D." Not topic labels. **Test:** if the paragraphs can be reordered without breaking the
   sentence, there is no argument yet, and that is the finding.
2. **One line per paragraph, naming its single claim.** A paragraph with two claims is two
   paragraphs or one cut.
3. **The paragraph you are asking for, slot by slot**, each slot a plain statement that stands
   on its own. **Test:** strip every *because*, citation and qualifier. If the bare statements no
   longer tell the story, the outline is a checklist rather than an argument.

Then: attach the *because* to the slots that owe one; name what you cut and where it is spent
instead; give the cut order in advance, saying which slots carry the argument; and check the
neighbouring sections for collisions first, because a beat already spent two pages earlier is
not available. In a collaborative proposal, **mark which group owns each slot**. Never open a
section on the applicants' own artefacts. Open on what changes in the field.
