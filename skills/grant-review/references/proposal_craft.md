# Proposal craft: the rules that travel between funders

These are the writing rules that hold whichever funder reads the proposal. They were first
written for the ERC, in the `erc-review` kit's `ERC_writing_guide.md`. This file keeps the
parts whose reasoning holds for any panel that scores a research proposal, and moves out
everything that depends on one call's readers, page limits or evaluation questions.

**How to tell a rule from a habit.** Each rule below rests on a reason about readers, and
the reason is what travels. "Objectives are knowledge claims" holds wherever a reviewer has
to say at the end whether an objective was met. "Do not argue feasibility in Part I" holds
only where the first reader is not scoring feasibility. That is true of an ERC Step-1 panel
and false of a BSF referee. Where a rule's force changes between funders, it carries a
**Varies:** line naming what decides it. Facts about a particular funder belong in that
funder's guide (`bsf-review/references/BSF_writing_guide.md`, or the ERC guide in
`erc-review`), not here.

The section numbers are stable, so the review protocol, the checker and the comment macros
can cite them: `craft §4` always means §4 of this file.

| § | Covers |
|---|---|
| [1](#1-the-reader-model) | who reads what, and how to build the model for a call |
| [2](#2-the-problem) | a nameable question · limitations vs barriers · falsifiable challenge · instability over gap |
| [3](#3-the-four-layers) | challenge/vision/aim · objectives · work units · tasks; vision vs aim |
| [4](#4-objectives) | 3–5 knowledge claims, interlinked, risk rising |
| [5](#5-state-of-the-art) | an argument in sub-areas, each ending on how the project moves past it |
| [6](#6-approach) | the logic of the route, and why this structure fits these questions |
| [7](#7-why-now-why-us-and-preliminary-results) | timeliness, preliminary results and how much of them, why these people |
| [8](#8-impact) | layered claims, with a *because* |
| [9](#9-the-work-plan) | project design · unit objective vs rationale · tasks · moonshots · risk · timeline |
| [10](#10-sentence-level-rules) | named causality, active voice where a person acts, and when passive is right |
| [11](#11-track-record-and-publication-lists) | what an entry must carry, and order and honesty |
| [12](#12-budget-and-resources) | budget as an argument, and where the numbers live |
| [13](#13-resubmission) | the response letter, and what time does to a resubmitted proposal |
| [14](#14-the-element-catalogue) | the elements reviewers expect in any research plan, and what each looks like in each field |

---

## 1. The reader model

Every rule in this file is chosen against a reader, so build the reader model before
applying any of them. For the call in hand, fill this table from the funder's own documents
and not from memory:

| Reader | How many | Expertise | Sees which documents | Scores which questions | Gets a reply? |
|---|---|---|---|---|---|

Funders differ on four questions, and each answer changes what a document has to do.

1. **Is there a stage that eliminates on a subset of the documents?** The ERC's Step 1 scores
   only Part B1. Wherever such a stage exists, everything that stage scores must be in the
   documents it sees (`review_protocol.md` stage 4). A funder that sends the whole package
   to every reviewer has no such stage, so the constraint shifts. Every page now has to
   survive an expert reading.
2. **Who are the readers: generalists, experts, or both?** Generalists need the question to
   matter before the method makes sense. Experts read the method first and will find the
   weak step. A document that one population reads must be written for that population. A
   document that both read needs a first page a generalist can score and later pages an
   expert cannot fault.
3. **How are scores combined?** "Median of three" forgives one hostile reader, and "a
   majority must say Excellent" does not. Where one serious objection moves a reviewer from
   the top grade, pre-empting objections is worth more than one more striking claim
   (`small_grants.md` §2).
4. **Can the applicant answer back?** An interview or rebuttal lets a misreading be
   corrected. Written reviews that are never rebutted mean every ambiguity is resolved
   against you, once.

**Varies:** everything in this section. Its job is to make the funder-specific answers
explicit before any other rule is applied.

## 2. The problem

### 2.1 The question is nameable

A reader who cannot state your question after one reading cannot argue for you. The test is
whether someone outside the subfield can write the question in one sentence after reading the
first page once, without help. If they cannot, move the question into the first paragraph and
cut whatever is there now, which is usually background or a widening generalisation.

### 2.2 Limitations versus barriers

Proposals routinely supply one and omit the other.

- **Limitations — what is not known.** Gaps in theory or understanding, open questions,
  unexplained observations.
- **Barriers — why it is not known.** No validated approach, no data at the needed
  resolution, equipment or compute that did not exist, two communities that never met.

Limitations alone read as "nobody got around to it", which leaves the reader wondering why
the project is needed now. The barrier is what makes the gap hard, and so it is also usually
the why-now argument (§7). In a collaborative proposal the barrier is often exactly what the
partnership removes: neither group alone has both the method and the system. Say so,
because that sentence then argues for the science and for the collaboration at once.

### 2.3 State the challenge in falsifiable terms

| Weak | Improved |
|---|---|
| "The mechanism of X is poorly understood." | "We do not know whether X is initiated by A or by B, because no assay resolves both on the relevant timescale." |
| "Current methods have limitations." | "Existing estimators are biased by Z whenever samples are dependent, which is every field dataset we know of." |

Replace *"X is poorly understood"* with what specifically is unknown plus why it is unknown.
"Poorly understood", "remains unclear", "little is known" and "has received limited
attention" mean the sentence has not been written yet. The checker flags them.

### 2.4 Prefer an instability to a gap

An opening built on a **gap** invites the reply "then fill a different one". An opening built
on an **instability** creates pressure: something the field believes that does not hold, two
results that cannot both be right, a method everyone uses that fails where it matters. Find
the "but" that the draft is hiding behind an "and".

## 3. The four layers

Every passage sits at one of four levels of abstraction. Confusing two adjacent levels is the
most common structural failure in any proposal.

```
Layer 1   Challenge · Vision · Aim · Impact        the why, and the after
Layer 2   Specific objectives                      3–5 knowledge claims
Layer 3   Work units / work packages / aims        how the objectives are attacked
Layer 4   Tasks                                    what you actually do
```

A funder with two documents usually wants layers 1–2 in the first and layers 3–4 in the
second. A funder with one research plan wants all four in one document, in that order, with
layer 1 short. In both cases a passage that describes a task where the reader expects an
objective reads as timidity, and a work unit with no objective above it has no purpose.

**Vision versus aim.** The vision outlives the grant, and the aim is what exists when the
grant ends. Write the vision, then the aim, then check that the aim is a genuine down-payment
on the vision rather than a restatement of it. A vision-shaped aim reads as unachievable and
an aim-shaped vision as unambitious. Both lose the same point.

**Varies:** how much of layer 1 a funder wants. A large single-investigator programme grant
wants a vision that would change a field. A small collaborative grant wants an aim that the
budget can plausibly buy, and a vision kept to two sentences (`small_grants.md` §3).

## 4. Objectives

- **A handful, interlinked, scaled to the pages that carry the method** (see *Varies* below):
  three to five in a long work plan, two or three in a 15-page plan. Too few reads as thin, and
  too many reads as a programme rather than a project. Say what depends on what, because five
  independent objectives read as five small projects.
- **Knowledge claims, not deliverables.** Use verbs of knowledge production: *determine
  whether, identify, quantify, reveal the mechanism by which, test*. Avoid *build, implement,
  release, apply*. When the output is an artefact, such as a database, model, tool or
  benchmark, name what the artefact lets anyone conclude. That conclusion is the objective.
- **Strike "to understand" and "to study".** Nothing about them can be checked at the end of
  the grant, and checkability is the one property an objective must have.
- **A bold standalone sentence, then two or three sentences of support.** The bold sentence
  is what a reviewer quotes back in a review, so it must survive being extracted. The
  sentences after it give the route and the links to the other objectives.
- **Order them so the risk rises.** A speculative objective placed first makes every later
  page be read under "what is left if this fails". Placed last, the same objective reads as
  upside. Say explicitly that the project is complete without it.
- **Related, but not blocking.** Each objective should yield a result even if an earlier one
  underperforms. One that only makes sense after another succeeds turns one failure into two.
- **Informative either way.** "Determine whether A matters" has one interesting outcome. "Compare
  the role of A in B and in C" informs whichever way it comes out.

**Varies:** the count, which scales with the pages that carry the method. A five-objective
programme fits a 14-page work plan. A 15-page single plan holds two or three, because each needs
about two pages of method an expert can check.

## 5. State of the art

An argument, not a survey.

- **Three or four sub-areas**, each under a visible heading, each mapping to an objective.
- **Four beats per sub-area:** current understanding and best approach → its specific
  limitation → the barrier that holds the field there → one sentence on how the project moves
  past it. Answer each barrier where it is raised, not only at the end of the section.
- **Your own work belongs inside it, and only inside it.** A state of the art that mainly
  cites the applicants reads as unfair to the field, and the reviewer most likely to notice is
  the one whose work is missing. Write a summary your competitors would sign.

**Varies:** length relative to the approach. A rule that survives every funder: **the approach
is at least as long as the state of the art**, because the balance is itself an argument about
whether the proposal cares more about what was done or about what you will do.

## 6. Approach

Make three things explicit: the **logic of the conceptual steps** and why each follows from
the last; how the strands, whether experimental, computational or theoretical, work
together; and **why this structure is the right fit for these questions**. Without the third,
the section is a list of activities rather than a strategy. That is the most common way this
section fails.

Add technical detail only where the logic is unintelligible without it. Protocols, sample
sizes and contingency plans belong in the work plan (§9).

**Varies:** where the approach ends and the work plan begins. In a two-document scheme the
first document carries only the logic. In a single research plan the approach section opens
the work plan and the two can merge, provided the logic is stated once at the top before any
task begins.

## 7. Why now, why us, and preliminary results

**Timeliness is argued, not asserted.** Name what changed: a method, a dataset, a result, your
own preliminary finding. "The field is ready" is not an argument. Anything public, such as a
new instrument, a released dataset or a published method, argues that the field is ready and
is equally available to competitors. Only your own results argue both that the field is ready
and that you are the one to do it.

**Preliminary results: the balance is where applicants go wrong, in both directions.** Too
much, and the hard part looks done and what remains looks like execution. None, behind a bold
claim, reads as wishful thinking. The strongest form is a preliminary result that *raises*
the project's question: "our data show A, which prompts two questions: does B, and can we
C?" Then say what the data do *not* settle. That sentence is your evidence and your
justification for the grant at once.

**Why us.** Two or three sentences even where a CV covers it: what each investigator brings
and why this team is placed to do this now. In a collaborative grant, the why-us answer is
*why this combination*, and it must say what each side cannot do alone (`small_grants.md`
§4).

**Varies:** how much preliminary data is expected. Schemes that fund a step change penalise
too much. Schemes whose referees score feasibility, which includes most small and
collaborative grants, penalise too little. Start-up and early-career tracks are often
explicit that none is required. Read the funder's instructions for the track.

## 8. Impact

- **Layer, do not spread.** Name the consequence that matters to *this* panel first and in
  detail, then wider fields as extensions. Impact claimed in every direction dilutes. The
  reader loses track of which consequence you believe in.
- **Every generalisation carries a *because*.** "These findings generalise to … because …" The
  *because*, a principle rather than a method, separates impact from hope.
- **End positively.** Impact is usually the last thing a reader sees in a section or document,
  so it sits in stress position.

**Varies:** whether societal or economic impact is scored. Some funders do not score it, and
there it earns space only after the scientific case. Some funders score it explicitly. NSF's
Broader Impacts criterion and the BSF's separate Broader Impacts Statement both make it an
address of its own. The word "impact" means different things to different funders, so read
the definition in the call.

## 9. The work plan

### 9.1 Project design

An overview before the detail: the number and function of the work units, which part is new,
and how the units interconnect and map to objectives. A figure mapping objectives to work
units, with dependencies drawn, answers "is this one project or a list of projects?" at a
glance. A table is enough if a figure will not fit.

### 9.2 Each work unit: objective versus rationale

- **Objective: what will exist when the unit is done.** One sentence, outcome-shaped.
- **Rationale: why the unit is needed.** Two to five sentences: the gap, uncertainty,
  bottleneck or dependency it addresses, plus preliminary data where relevant.

The classic error is writing the rationale and labelling it the objective:

> ✗ "To address the lack of robust biomarkers…" ← that is why the unit exists
>
> ✓ "To identify and validate biomarkers that predict progression within 12 months."

Close each unit with **expected outcomes**: what the field has afterwards that it lacks now.

### 9.3 Tasks

A task is a compact scientific story, written as prose, not as sub-headings:

1. **Purpose** (1–2 sentences): the question the task answers.
2. **Approach** (4–8 sentences): the experiments, analyses or derivations.
3. **Contribution** (1–3 sentences): not "deliver a dataset" but "the first taxonomy of X".
4. **Link** (optional, 1 sentence): what the result motivates next.

**Do not recurse.** The unit's objective and rationale apply to its tasks, so a task needs no
objective/rationale/outcome block of its own. Three cheap details carry most of the weight:
**name who does it**, which connects the plan to the budget and, in a collaborative grant, to
the collaboration; **include the check**, meaning how you will know the step worked; and
**give the task-level fallback** in one clause where the risk is specific to this task.

### 9.4 Moonshot tasks

The one deliberately high-risk task in a unit gets five moves instead of three: the question
or opportunity, why it is plausible, a bounded first approach, **what success and failure
each teach**, and the decision point that bounds it. Do not apologise for the risk. Say it is
deliberately high-risk *because* of what it would establish. State that the unit is complete
without it, so that the moonshot raises the ceiling without lowering the floor. Keep it
shorter than a core task, but longer than one line. "We will also explore X" reads as an
afterthought.

**Varies:** whether a moonshot belongs at all. In a small grant whose referees grade
realism, one bounded moonshot can lift the proposal. Two will read as over-promising on a
budget that cannot carry them (`small_grants.md` §3).

### 9.5 Risk

A risk strategy, not a table of platitudes. Technical risks go in a short table, with
probability, impact, contingency and the expected outcome of plan B beside plan A. Conceptual
risk, where the central hypothesis does not hold, goes in a paragraph answering what the
project still establishes if you were wrong. A negative result that settles a live question
is a result, and a project that only works if you were right is a gamble. **Ask why the risk
is worth taking.** That question turns a defensive section into an ambitious one. Do not end
a document on risk. Close with a short concluding paragraph that holds the case for funding
in the last position.

### 9.6 Timeline

Show decision points, not just durations. A go/no-go moment marked on the chart answers the
reviewer who asks "what if step 2 fails?" before they write it down. Many funders also
collect the schedule in a form outside the narrative. Keep the two consistent.

## 10. Sentence-level rules

**Make cause and effect explicit.** Replace every *and* and *then* that does causal work with
a connective that names the relation:

> Weaker: "We will collect data and then build a reference library."
>
> Better: "We will collect data *in order to* build a reference library, *which in turn lets
> us* …"

A chain of *and … then … and* gives the reviewer no way to tell a plan with a logic from a
list, and a list is what an incremental project looks like.

**Active voice where a person acts.** "The correlation will be measured" → "We will measure
the correlation". In a collaborative proposal, name *which* team acts: "the Haifa group will
measure, and the Boston group will model". This is also how the plan shows the collaboration
working. **Keep the passive** where nobody acts ("the hypothesis is rejected if …"), and
where the passive subject is the thread the paragraph follows. Test before converting: read
the first six words of the converted sentence and of the next. If the link between them was
in the passive subject, keep the passive.

**A repeated opener marks a set or it marks nothing.** Three consecutive "we will" openers
in a work plan are a tic, because the agent is constant. Three consecutive "Regardless of X"
openers after "we test three invariances" are the device working. Do not fix this by quota.

**Every claim is cited, shown, or softened**, including those in subordinate clauses ("widely
believed"). Never invent a citation to support one.

**Emphasis is a separate pass.** These rules make a sentence carry its meaning. They do not
decide which sentence a reader still carries an hour later. That is the `grant-writing`
skill in `erc-review`, and it runs after the review stages.

## 11. Track record and publication lists

- **Every listed output earns its place.** Where the format allows annotation, give its
  significance, your role, and its relevance to *this* project. A bare citation does none of
  that work.
- **Report authors exactly as published:** all of them, in order, with joint first or
  corresponding authorship marked. Trimming a list or promoting yourself is a discrepancy a
  reviewer checks and cannot unsee.
- **Select for relevance and recency** when a page cap forces a choice. The cap is the
  funder telling you to choose.
- **No journal impact factors.** Most funders now assess outputs on their own merits. Citation
  counts and competitive selectivity figures for things you *won* are different, and count.
- **Non-paper outputs count.** Datasets, software, benchmarks and shared tasks are often the
  stronger evidence of field-level influence in computational fields. Claim them explicitly.

## 12. Budget and resources

A budget is an argument that the plan is real. Three rules travel.

- **Every major line ties to a task**, and every person in the plan appears in the budget or
  in a sentence saying who pays for them. Reviewers read the work plan and the budget side by
  side.
- **Justify, do not list.** A headcount is not a justification. Give each line a profile and
  a responsibility.
- **Say what the grant does not pay for.** Existing equipment, other grants and institutional
  support make a small request credible for a large plan. They must not overlap with what you
  request.

**Varies:** almost everything else. Caps, overhead rates, salary eligibility, equipment
rules, and whether budget text may appear in the narrative at all. These live in the funder
guide.

## 13. Resubmission

A resubmission is read by a mix of new reviewers and some who read the first version. Write
for both.

- **The response letter answers the substance, not the reviewer.** Quote only the sentence
  you are answering, then say what changed and where. Copying whole reviews buries the
  changes.
- **Concede first, then show the change.** "The reviewer is right that the sample was
  underpowered; Task 2.1 now uses N = … (p. 7)" persuades. Arguing that the reviewer misread
  rarely does, even when they did. The new reviewers did not see the misreading, and the old
  ones will not enjoy being corrected.
- **Time has passed.** Re-check the state of the art, the timeliness argument and any claim
  of novelty against what was published since the last round. A resubmission that ignores a
  year of literature reads as stale to exactly the reviewers who flagged it.
- **A changed proposal is not a new proposal.** Funders that cap resubmissions usually also
  reject a lightly edited old proposal submitted as new. Check the funder's rule before
  relabelling.

## 14. The element catalogue

Whatever a funder calls its sections, reviewers of a research plan look for the same dozen
elements. A funder guide maps them to its own headings: the BSF's map is `bsf-review` guide
§4.12. This section defines each element once and says what it looks like in fields where the
biomedical template, built around a central hypothesis, fits badly. **Translate an element;
do not drop it.** A mathematics plan with no hypothesis still needs the thing the hypothesis
does, a claim that can turn out wrong.

| Element | What it does | Fails when |
|---|---|---|
| **Question** | one sentence a neighbouring-field reader can repeat (§2.1) | the plan states a topic |
| **Long-term goal** | the direction beyond this grant (§3) | it is the aim restated, or the aim is it |
| **Central hypothesis**, or its translation | the claim the plan can show wrong | nothing in the plan could fail |
| **Gap and barrier** | what is unknown and why (§2.2) | the gap is an omission no one tried |
| **Preliminary evidence** | plausibility and feasibility in these hands (§7) | absent where feasibility is scored; or the main result is already in |
| **Objectives** | what will be known (§4) | a process, a deliverable, or the tasks renamed |
| **Approach** | the route and why it fits (§6) | "apply method X to problem Y" with no question X answers |
| **Success criterion** | what result counts, stated in advance | success means "the work was done" |
| **Pitfalls and alternatives** | technical fallbacks and alternative interpretations (§9.5) | "alternative approaches will be considered" |
| **Timeline and milestones** | results by date, with decision points (§9.6) | bars per objective lasting the whole grant |
| **Team and resources** | why these people, and what else pays (§7, §12) | boilerplate facilities; other grants omitted |
| **Significance and payoff** | what changes if it works, with a *because* (§8) | it repeats the background |

### What each element looks like by field

| Element | Experimental sciences | Mathematics and theory | Empirical computer science | Social sciences |
|---|---|---|---|---|
| Central hypothesis | a mechanistic claim, often "distinguish between A and B" | the **key new idea** that should crack a named problem or conjecture; naming a famous problem is not enough | either a hypothesis ("method X generalises across Y because Z") or a technology-driven claim (an open technical problem and why this approach solves it); one question must unify the aims | a directional, theory-derived prediction, in a design that lets the PI be wrong |
| Objectives | "determine", "quantify", not "study" | a **graded ladder of problems**: some within reach, some harder, one very hard | about three, each with its own evaluation | tied to a theoretical contribution; not "explore", "expand" or "develop", which read as preliminary |
| Preliminary evidence | the technique working in your lab; data that make the hypothesis plausible | special cases proved, partial results, computations; the idea shown to get traction, short of a proof | a prototype or pilot with numbers against a baseline | pilot data or survey, data-access permissions in hand, power estimates |
| Approach | experiments mapped to the hypothesis, with controls and statistics | the obstacles and the tools for each, at a level a non-specialist panel can follow | concrete methods and an evaluation design | the design, the sample, and how the analysis answers the question; in economics, the identification strategy |
| Success criterion | the result that supports or rejects the hypothesis, with a threshold | a theorem proved, or the conjecture settled in a stated case | a measurable gain on named held-out data, read as a research finding, not an engineering output | a pre-specified analysis and a falsifiable prediction; power with a justified effect size |
| Pitfalls | technical failure and alternative explanations | built into the ladder: a weaker statement, a special case, another technique | the failure mode (data, model, scale) and a fallback; a negative result analysed as a finding | limitations acknowledged; alternative data or identification; a plan for low power |
| Timeline | realistic, with dependencies | light; problems mapped to years and students | dependencies between aims shown | fieldwork, ethics approval and data-release dates |
| Resources | equipment, sites, samples, facility access | people and track record | compute, data, annotation, users | data access, ethics approval, recruitment |

**The common complaints, by field.** In theory: goals stated without what achieving them would
mean, which a former NSF mathematics programme officer called the leading cause of failure; and
a problem list with nothing likely to succeed. In empirical computer science: engineering
delivery read as research, metrics that count outputs, and no single question across the aims;
and the related work an expert panellist knows that the proposal missed. In the social sciences:
exploratory framing, a design that cannot falsify, and data access not shown. In the experimental
sciences: over-ambition for the years available, and a background pasted together from
earlier papers.

**Sources.** NIH Specific Aims practice as taught by grants offices (University of Oregon, 2022;
UC Irvine, 2021) and NIAID review guidance; NCI and NINDS milestone guidance; J. Brennan, *NSF
proposal preparation: the view of an ex-program officer*, AMS Notices, 2007; UCLA Mathematics
grant workshop, 2021; C. Grimm (NSF panellist), CAREER advice; L. Anthony, composite NSF CAREER
reviews, 2025; NSF Sociology and Economics programme checklists (archived) and M. Cornwall, NSF
SBE tips, 2017; M. Gutnick, tips for Israeli grant proposals. These are practitioner and funder
advice for analogous schemes, not rules of any one funder.

