# BSF overlay for the emphasis pass

The `grant-writing` skill in `erc-review` decides what a reader should carry away, and marks it
with thirteen devices (D1–D13) measured over 17 funded ERC and 13 funded NIH documents. Its
`funders.md` holds one section per funder, and the BSF has none, because no BSF documents were
coded. This file is that section, written in the same shape so it can be pasted into
`funders.md` as `# BSF`.

**Nothing below is measured.** Every line is a reading of the BSF's documented review process
(`BSF_writing_guide.md` §5–§6) against the reasoning in each device entry. It is *direction*,
not *rate*. The `grant-writing` rule therefore stands as written: the devices and their
corpus numbers apply, and this overlay says only where the BSF's readers make a reading weaker,
stronger or inverted. Treat it as advice until someone codes funded BSF plans.

---

# BSF

## What the documents are

**One argument document and one plan document are the same file.** The research plan is read in
full by 3–5 expert referees, then the panel ranks from their reviews. No reader sees only part
of it. Two consequences for every device:

- **Survival under one fast reading matters less, and survival under a hostile careful reading
  matters more.** The `ranking.md` axis that dominates is **doubted**, not **remembered**: at a
  majority-Excellent threshold, one unsupported claim quoted in a review costs more than a
  forgettable true one (`small_grants.md` §2).
- **The panel's fast reading happens on the abstract and the first page**, and on the
  referees' summaries. Spend memory devices there, not spread through fifteen pages.

## The ranking gate, with a BSF row

Add a claim to the ranked list that the ERC and NIH legs never needed: **the collaboration
claim**, what the two groups achieve together that neither could alone. It is judged on
criterion C, which is a separate gate. Usually it is doubted, because referees have read many
nominal collaborations, so its support (D9, D13) runs before any memory device.

## D1 — headings

The five required items (`BSF_writing_guide.md` §4) are **mandated labels**. Keep them, and use
the route *keep the label, add the content*: "3. Methodology and plan of operation: two sites,
one causal model". The *drop the label* route available at the ERC is not safe here, because
the BSF says applications lacking any item "will not be considered", and a reader looking for
item 4 should find it by its number.

## D2 — bold inside a sentence

The ERC habit (median 26 spans) has no BSF evidence behind it. Spacing at 1.5 and 12 pt already
makes the page airy, so a dense bold layer reads as shouting to an expert referee. Default to the
NIH-like range: a few spans, at the obstacle sentence and at each objective's standalone claim
(craft §4). The obstacle sentence remains the most consistent site, and that reading travels.

## D5 — hedge restraint

Stronger than at the ERC, for a BSF-specific reason. The plan is the only document, so there is
no "argument document states, plan document qualifies" split to manage. Every hedge on a method
you have chosen is read by the expert who decides between Excellent and Very Good. Keep hedges
for genuine uncertainty, and put that uncertainty in item 4 with its fallback rather than
spreading it through item 3.

## D7 — `I will`

Usually **inverts** here. The BSF scores two groups collaborating, and the useful voice is
neither "I" nor a blanket "we" but **the named group**: "the Haifa group will …", "the Michigan
group will …" (`BSF_writing_guide.md` §7). Keep "we" for joint actions, where it is information.
The singular is right only in a start-up, for the junior PI's own track, and even there the senior
partner's role must be named.

## D8, D9, D13 — the number, prior results, the concrete example

These are the devices that answer **doubted**, so they carry more weight than in the corpus legs.
D9's reading is closest to the NIH leg's floor: plans whose referees score feasibility rest
claims on the groups' own results. **Use D9 for both groups.** A plan where only one site has
prior results reads as one lab's project with a partner attached, which costs criterion C. In a
start-up, preliminary results are not required (§12 of the guide), and D9 shifts to the senior
partner's environment and the junior PI's own prior work.

## D10 — a figure

Expect to carry figures in physical, life and computational panels, as in the corpus. One figure
is BSF-specific and worth its space in every field: **the two-site handoff diagram** (guide §7).
It is the cheapest answer to criterion C(a).

## What this overlay cannot tell you

There are no rates. If you can assemble funded BSF research plans, with the PIs' permission, run
`emphasis_measure.py --tsv` over them and replace this section's directions with numbers in the
same form as the ERC and NIH sections.
