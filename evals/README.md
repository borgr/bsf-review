# Evaluations

Four scenarios, one per claim worth defending. They are in the same format as `erc-review`'s
evals: a query, the files it runs against, the behaviour a pass requires
(`expected_behavior`, each graded independently), and the wrong answers that look right
(`failure_modes`). There is no runner. Run them by hand or feed them to a judge.

```sh
cd <the scenario's cwd>
claude "<the scenario's query>"
```

| File | Runs on | Tests |
|---|---|---|
| `01-cooperation-is-a-gate.json` | `example/` | The stop rule, with the BSF's cooperation criterion as a stage-1 shape problem rather than a wording issue, and no invented roles. |
| `02-feasibility-flips-at-bsf.json` | `fixtures/erc-habits-at-bsf/` | That a general rule is applied with this funder's force. At the BSF, feasibility and fallbacks are scored and oversized ambition costs a grade, the reverse of the ERC Step-1 advice. |
| `03-fixes-format-and-reruns.json` | `example/` | Stage 9 handled mechanically, including the `\onehalfspacing` line-count trap, with a re-run and no content invented. |
| `04-structures-a-theory-plan.json` | `templates/bsf/` | Planning, not reviewing: the section-by-section structure and element map handed back translated for a field without hypotheses, with nothing invented. |

What to watch for, in order of how often it goes wrong: **did it stop** at the highest failing
stage; **does every finding name a criterion and a reader**; **did it invent** a role, result,
citation or resource; **did it edit above stage 8**; and, BSF-specific, **did it import an ERC
rule** without checking the funder guide.

The unit tests for the checker are in `skills/grant-review/tools/test_grant_check.py`:

```sh
python3 -m unittest discover -s skills/grant-review/tools
```
