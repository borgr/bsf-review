"""Tests for grant_check.py. Run: python3 -m unittest test_grant_check (from tools/)."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import grant_check as gc  # noqa: E402

BSF = gc.load_profile("bsf")
ERC = gc.load_profile("erc")

PLAN_OK = r"""\documentclass[12pt,a4paper]{article}
\usepackage[margin=2cm]{geometry}
\linespread{1.5}
\begin{document}
\section*{Research Plan}
\section{Background}
Sediment communities in Israel and the U.S. differ in drought history.
\section{Objectives and significance}
O1. Determine whether recovery depends on drought history.
\section{Methodology and plan of operation}
The Israeli group samples; the U.S. group models. The collaboration is interdependent.
\section{Risk analysis and alternative paths}
If sampling fails we use archived cores.
\section{Resources}
Both groups hold sequencers and field equipment.
We used generative AI only for copy-editing.
\end{document}
"""


def codes(findings):
    return {f.code for f in findings}


def make_docx(path: pathlib.Path, paras: list[str], sz_half_pts=24, line=360, margin_twips=1134):
    """A paragraph written "## Title" gets the Heading 2 style, as Word would store it."""
    def para(p):
        h = len(p) - len(p.lstrip("#"))
        style = f'<w:pPr><w:pStyle w:val="Heading{h}"/></w:pPr>' if h else ""
        return f"<w:p>{style}<w:r><w:t>{p.lstrip('# ')}</w:t></w:r></w:p>"
    body = "".join(para(p) for p in paras)
    doc = (f'<w:document xmlns:w="w"><w:body>{body}<w:sectPr><w:pgMar w:top="{margin_twips}" '
           f'w:bottom="{margin_twips}" w:left="{margin_twips}" w:right="{margin_twips}"/>'
           f"</w:sectPr></w:body></w:document>")
    styles = (f'<w:styles xmlns:w="w"><w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="{sz_half_pts}"/>'
              f'</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:line="{line}" w:lineRule="auto"/>'
              f"</w:pPr></w:pPrDefault></w:docDefaults></w:styles>")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", styles)
        z.writestr("docProps/app.xml", "<Properties><Pages>17</Pages></Properties>")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def doc(self, name, text, part="research_plan"):
        p = self.dir / name
        p.write_text(text, encoding="utf-8")
        return gc.read_doc(part, p)

    def run_bsf(self, doc):
        return gc.check_general(doc, set()) + gc.check_profile(doc, BSF["parts"][doc.part], BSF)


class LinesPerPage(Base):
    def test_onehalfspacing_breaks_38_line_cap(self):
        d = self.doc("research_plan.tex", PLAN_OK.replace(r"\linespread{1.5}",
                                                          "\\usepackage{setspace}\n\\onehalfspacing"))
        self.assertIn("lines-per-page", codes(self.run_bsf(d)))

    def test_linespread_15_is_within_cap(self):
        f = self.run_bsf(self.doc("research_plan.tex", PLAN_OK))
        self.assertNotIn("lines-per-page", codes(f))
        self.assertNotIn("spacing-single", codes(f))

    def test_single_spacing_and_11pt_block(self):
        src = PLAN_OK.replace("12pt", "11pt").replace(r"\linespread{1.5}", "")
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertTrue({"font-small", "spacing-single"} <= c)

    def test_narrow_margin_blocks(self):
        c = codes(self.run_bsf(self.doc("research_plan.tex", PLAN_OK.replace("margin=2cm", "margin=1.5cm"))))
        self.assertIn("margin-small", c)


class RequiredContent(Base):
    def test_clean_plan_has_no_block(self):
        f = self.run_bsf(self.doc("research_plan.tex", PLAN_OK))
        self.assertEqual([x for x in f if x.severity == "BLOCK"], [])

    def test_headings_count_as_addresses(self):
        # "Resources" appears only as a \section heading: still an address.
        src = PLAN_OK.replace("Both groups hold sequencers and field equipment.", "None listed yet.")
        self.assertNotIn("item5-resources", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_missing_us_role_blocks(self):
        src = PLAN_OK.replace("the U.S. group models", "a partner models").replace("and the U.S.", "")
        self.assertIn("item3-us-role", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class Patterns(Base):
    def test_we_will_run_spans_source_lines(self):
        src = PLAN_OK.replace("If sampling fails we use archived cores.",
                              "We will sample cores. We will extract DNA.\nWe will sequence them.")
        self.assertIn("we-all-the-way", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_overhead_either_order(self):
        for s in ("We add 25\\% overhead.", "Overhead is charged at 20\\%."):   # bare % is a TeX comment
            src = PLAN_OK.replace("If sampling fails we use archived cores.", s)
            self.assertIn("budget-overhead", codes(self.run_bsf(self.doc("research_plan.tex", src))), s)

    def test_erc_feasibility_rule_is_b1_only(self):
        b1 = self.doc("b1.tex", "\\begin{document}\nThe approach is feasible.\n\\end{document}", part="b1")
        b2 = self.doc("b2.tex", "\\begin{document}\nThe approach is feasible.\n\\end{document}", part="b2")
        self.assertIn("feasible-assertion", codes(gc.check_profile(b1, ERC["parts"]["b1"], ERC)))
        self.assertNotIn("feasible-assertion", codes(gc.check_profile(b2, ERC["parts"]["b2"], ERC)))


class WordLimits(Base):
    def test_abstract_hard_limit_blocks(self):
        d = self.doc("abstract.md", "# Abstract\n\n" + "word " * 260 + "contribution.", part="abstract")
        f = [x for x in self.run_bsf(d) if x.code == "over-words"]
        self.assertEqual(f[0].severity, "BLOCK")

    def test_impact_about_limit_scores(self):
        d = self.doc("broader_impacts.md", "# Broader Impacts Statement\n\n" + "word " * 270,
                     part="broader_impacts")
        f = [x for x in self.run_bsf(d) if x.code == "over-words"]
        self.assertEqual(f[0].severity, "SCORE")


class Docx(Base):
    def test_docx_format_and_pages(self):
        p = self.dir / "research_plan.docx"
        make_docx(p, ["Research Plan", "The mechanism is poorly understood."], sz_half_pts=22, line=240,
                  margin_twips=850)
        d = gc.read_doc("research_plan", p)
        c = codes(self.run_bsf(d))
        self.assertTrue({"font-small", "spacing-single", "margin-small", "vague-challenge"} <= c)
        self.assertEqual(gc.page_count(d)["pages"], 17)

    def test_compliant_docx_passes_format(self):
        p = self.dir / "research_plan.docx"
        make_docx(p, ["Research Plan", "Text."])
        c = codes(self.run_bsf(gc.read_doc("research_plan", p)))
        self.assertFalse({"font-small", "spacing-single", "margin-small"} & c)


class Resolve(Base):
    def test_stems_map_files_to_parts(self):
        for name in ("my_research_plan.tex", "abstract.md", "broader_impacts.txt", "notes.txt"):
            (self.dir / name).write_text("x", encoding="utf-8")
        parts = {d.part: d.path.name for d in gc.resolve(BSF, [str(self.dir)])}
        self.assertEqual(parts["research_plan"], "my_research_plan.tex")
        self.assertEqual(parts["broader_impacts"], "broader_impacts.txt")
        self.assertNotIn("notes.txt", parts.values())


class Collaboration(Base):
    def test_task_without_group_is_flagged(self):
        src = PLAN_OK.replace("If sampling fails we use archived cores.",
                              "\\paragraph{Task 2.1: Assay.}\nWe sequence every core and compare the "
                              "recovery curves across all four sites over three seasons. Each core "
                              "is processed within a day of collection.")
        f = [x for x in self.run_bsf(self.doc("research_plan.tex", src)) if x.code == "task-owner"]
        self.assertEqual(len(f), 1)

    def test_task_with_lead_line_passes(self):
        src = PLAN_OK.replace("If sampling fails we use archived cores.",
                              "\\paragraph{Task 2.1: Assay.}\nWe sequence every core and compare the "
                              "recovery curves across all four sites over three seasons. Led by the "
                              "Haifa group, with the Michigan student.")
        self.assertNotIn("task-owner", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class Resubmission(Base):
    def test_defensive_letter_without_summary(self):
        d = self.doc("resubmission_letter.md",
                     "# Resubmission Letter\n\nThe reviewer missed our pilot data, as clearly stated.",
                     part="resubmission_letter")
        c = codes(self.run_bsf(d))
        self.assertTrue({"resub-summary", "resub-panel", "resub-locations", "defensive-reply"} <= c)

    def test_good_letter_passes(self):
        d = self.doc("resubmission_letter.md",
                     "# Resubmission Letter\n\nSummary of major changes: the panel asked for a fallback; "
                     "Section 3.2 (p. 9) now gives one.", part="resubmission_letter")
        c = codes(self.run_bsf(d))
        self.assertFalse({"resub-summary", "resub-panel", "resub-locations", "defensive-reply"} & c)


class Structure(Base):
    def test_container_heading_is_not_unwritten(self):
        d = self.doc("research_plan.tex",
                     "\\begin{document}\n\\section{Plan}\n\\subsection{WP1}\nText here.\n\\end{document}")
        flags = {u["title"]: u["flag"] for u in gc.structure_units(d)}
        self.assertEqual(flags["Plan"], "")


TEMPLATES = pathlib.Path(__file__).resolve().parents[3] / "templates" / "bsf"

FILLER_WORDS = " ".join(["The sites differ in rainfall history and in soil texture."] * 14)  # past the 120-word block minimum


def block(title, body):
    return f"\\subsection{{{title}}}\n{body} {FILLER_WORDS}\n"


def plan(opening, sections):
    return ("\\documentclass[12pt,a4paper]{article}\n\\usepackage[margin=2cm]{geometry}\n"
            "\\linespread{1.5}\n\\begin{document}\n\\section*{Research Plan}\n"
            + opening + "\n" + sections + "\n\\end{document}\n")


class Opening(Base):
    def test_hypothesis_on_page_one_passes(self):
        src = plan("Our central hypothesis is that history sets recovery. Objective 1: determine it. "
                   "The Israeli and U.S. groups need each other.", "\\section{Background}\nText.")
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertFalse({"opening-hypothesis", "opening-objectives", "opening-collaboration"} & c)

    def test_hypothesis_buried_after_page_one(self):
        src = plan("\\section{Background}\n" + "word " * 500,
                   "\\section{Objectives}\nWe test the hypothesis that history sets recovery.")
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertIn("opening-hypothesis", c)
        self.assertNotIn("hypothesis-stated", c)


class ObjectiveBlocks(Base):
    def test_block_without_success_or_pitfalls(self):
        src = plan("", "\\section{Methodology}\n" + block("Objective 1: Recovery", "We sample cores."))
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertTrue({"objective-success", "objective-pitfalls"} <= c)

    def test_complete_block_passes(self):
        body = ("The hypothesis is supported if the slope is negative. "
                "If extraction fails, the Davis group samples the wetter plots.")
        src = plan("", "\\section{Methodology}\n" + block("Objective 1: Recovery", body))
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertFalse({"objective-success", "objective-pitfalls"} & c)

    def test_criterion_in_nested_paragraph_counts(self):
        src = plan("", "\\section{Methodology}\n\\subsection{Objective 1: Recovery}\n"
                   "\\paragraph{Task 1.1: Sampling.} " + FILLER_WORDS +
                   "\n\\paragraph{Expected outcomes.} Success means a negative slope."
                   "\n\\paragraph{Pitfalls.} If extraction fails we use archived cores.\n")
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertFalse({"objective-success", "objective-pitfalls"} & c)

    def test_short_mention_is_not_a_block(self):
        src = plan("", "\\section{Objectives}\n\\subsection{Objective 1: Recovery}\nDetermine it.\n")
        self.assertNotIn("objective-success", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class ObjectiveCount(Base):
    def test_five_objectives_flagged(self):
        src = plan("Objective 1 to Objective 5 together test it.", "")
        self.assertIn("too-many-objectives", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_chemistry_is_not_an_objective(self):
        src = plan("Objective 1 tests it. O6-methylguanine and O5 sites are measured.", "")
        self.assertNotIn("too-many-objectives", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_three_objectives_pass(self):
        src = plan("Objective 1, Objective 2 and Objective 3 together test it.", "")
        self.assertNotIn("too-many-objectives", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class Proportions(Base):
    def test_methods_shorter_than_background(self):
        src = plan("", "\\section{Background}\n" + "word " * 300 + "\n\\section{Methodology}\n" + "word " * 100)
        self.assertIn("methods-share", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_methods_longer_passes(self):
        src = plan("", "\\section{Background}\n" + "word " * 100 + "\n\\section{Methodology}\n" + "word " * 300)
        self.assertNotIn("methods-share", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class ObjectiveVerbs(Base):
    def test_understand_is_flagged_determine_is_not(self):
        d = self.doc("research_plan.md", "# Research Plan\n\nObjective 1: To understand recovery.\n\n"
                     "Objective 2: Determine whether history sets recovery.\n")
        lines = [f.line for f in gc.check_general(d, set()) if f.code == "objective-open-verb"]
        self.assertEqual(lines, [3])


class Labels(Base):
    def test_label_forms(self):
        flagged = ["**Objective 1:** To study X.", "Specific Aim 1: To study X.", "Aim 1.2: To study X.",
                   "\\textbf{Problem II:} To understand X.", "O1. To study X."]
        clean = ["O3 study of ozonolysis.", "Objective 1: Determine whether X.", "Goals are to study X."]
        for text, want in [(t, True) for t in flagged] + [(t, False) for t in clean]:
            d = self.doc("research_plan.md", "# Research Plan\n\n" + text + "\n")
            got = "objective-open-verb" in codes(gc.check_general(d, set()))
            self.assertEqual(got, want, text)

    def test_deliverable_with_bold_label(self):
        d = self.doc("research_plan.md", "# Research Plan\n\n**Aim 3:** Build a model.\n")
        self.assertIn("objective-deliverable", codes(gc.check_general(d, set())))

    def test_lowercase_us_is_not_the_us_partner(self):
        src = PLAN_OK.replace("the U.S. group models", "a partner models").replace("and the U.S.", "")
        src = src.replace("If sampling fails", "Let us say: if sampling fails")
        self.assertIn("item3-us-role", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class ReviewFixes(Base):
    def test_markdown_comments_are_not_content(self):
        d = self.doc("research_plan.md", "# Research Plan\n\n<!-- give a timeline with milestones -->\n\nText.\n")
        self.assertIn("timeline", codes(self.run_bsf(d)))

    def test_item2_objectives_are_not_blocks(self):
        src = plan("", "\\section{Objectives and significance}\n" + block("Objective 1: Recovery", "We sample.")
                   + "\\section{Methodology}\n" + block("Objective 1: Recovery",
                   "Success means a negative slope. If extraction fails we use archived cores."))
        f = [x for x in self.run_bsf(self.doc("research_plan.tex", src)) if x.code == "objective-success"]
        self.assertEqual(f, [])

    def test_items_as_subsections_under_a_numbered_title(self):
        src = plan("", "\\section{Research Plan}\n\\subsection{Background}\n" + "word " * 300 +
                   "\n\\subsection{Objectives}\nText.\n\\subsection{Methodology}\n" + "word " * 100)
        self.assertIn("methods-share", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_unrecognised_headings_say_so(self):
        src = plan("", "\\section{Introduction}\n" + "word " * 50 + "\n\\section{Next}\nText.")
        self.assertIn("methods-share-unknown", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_opening_stops_at_item_1(self):
        src = plan("Some context.", "\\section{Background}\nWe test the hypothesis that X; Objective 1 does.")
        c = codes(self.run_bsf(self.doc("research_plan.tex", src)))
        self.assertTrue({"opening-hypothesis", "opening-objectives"} <= c)

    def test_small_in_body_is_flagged(self):
        src = plan("", "\\section{Methodology}\n\\begin{center}\\small\nA table.\n\\end{center}")
        self.assertIn("font-small-runs", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_collaboration_needs_a_heading(self):
        src = plan("", "\\section{Methodology}\nWe use a joint distribution and cooperative binding.")
        self.assertIn("collaboration-section", codes(self.run_bsf(self.doc("research_plan.tex", src))))

    def test_docx_headings_feed_structure_checks(self):
        p = self.dir / "research_plan.docx"
        make_docx(p, ["# Research Plan", "## Methodology", "### Objective 1: Recovery",
                      "We sample cores. " + FILLER_WORDS])
        c = codes(self.run_bsf(gc.read_doc("research_plan", p)))
        self.assertTrue({"objective-success", "objective-pitfalls"} <= c)


class SecondReview(Base):
    def test_word_heading1_items_heading2_aims(self):
        p = self.dir / "research_plan.docx"
        make_docx(p, ["# Research Plan", "Opening.", "# 1. Background", "Text.",
                      "# 3. Methodology", "## Aim 1: Recovery", "We sample cores. " + FILLER_WORDS])
        f = [x for x in self.run_bsf(gc.read_doc("research_plan", p)) if x.code == "objective-success"]
        self.assertEqual([x.line for x in f], [6])

    def test_line_points_at_the_item3_block_not_item2(self):
        src = ("# Research Plan\n\n## 2. Objectives\n\n### Aim 1: Recovery\n\nShort.\n\n"
               "## 3. Methodology\n\n### Aim 1: Recovery\n\nWe sample. " + FILLER_WORDS + "\n")
        f = [x for x in self.run_bsf(self.doc("research_plan.md", src)) if x.code == "objective-success"]
        self.assertEqual([x.line for x in f], [11])

    def test_introduction_can_be_the_opening(self):
        src = ("# Research Plan\n\n## Introduction\n\nWe test the hypothesis that X. Objective 1 does; "
               "neither group can do it alone.\n\n## 1. Scientific background\n\nText.\n")
        c = codes(self.run_bsf(self.doc("research_plan.md", src)))
        self.assertFalse({"opening-hypothesis", "opening-objectives", "opening-collaboration"} & c)

    def test_localized_word_heading_style(self):
        p = self.dir / "research_plan.docx"
        body = ('<w:p><w:pPr><w:pStyle w:val="berschrift1"/></w:pPr><w:r><w:t>Research Plan</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="berschrift2"/></w:pPr><w:r><w:t>Methodology</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Text.</w:t></w:r></w:p>')
        styles = ('<w:styles xmlns:w="w"><w:style w:type="paragraph" w:styleId="berschrift1">'
                  '<w:name w:val="heading 1"/></w:style><w:style w:type="paragraph" w:styleId="berschrift2">'
                  '<w:name w:val="heading 2"/></w:style></w:styles>')
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("word/document.xml", f'<w:document xmlns:w="w"><w:body>{body}</w:body></w:document>')
            z.writestr("word/styles.xml", styles)
        titles = [u["title"] for u in gc.structure_units(gc.read_doc("research_plan", p))]
        self.assertEqual(titles, ["Research Plan", "Methodology"])

    def test_determiner_is_not_a_lead_group(self):
        src = PLAN_OK.replace("If sampling fails we use archived cores.",
                              "\\paragraph{Task 2.1: Assay.}\nThe team sequences every core. " + FILLER_WORDS)
        self.assertIn("task-owner", codes(self.run_bsf(self.doc("research_plan.tex", src))))


class Headings(Base):
    def test_run_in_paragraph_is_not_a_task(self):
        src = plan("", "\\section{Objectives}\n\\paragraph{Significance.} " + FILLER_WORDS)
        f = self.run_bsf(self.doc("research_plan.tex", src))
        self.assertNotIn("task-owner", codes(f))

    def test_template_slot_is_a_placeholder_not_a_note(self):
        d = self.doc("research_plan.tex", plan("[[Stakes, one sentence.]]", ""))
        c = codes(gc.check_general(d, set()))
        self.assertIn("placeholder", c)
        self.assertNotIn("stray-note", c)


class Templates(unittest.TestCase):
    """The skeletons are compliant: every finding is an unfilled slot."""

    def test_skeletons_have_only_slot_findings(self):
        for name in ("research_plan.tex", "research_plan.md", "research_plan.docx"):
            path = TEMPLATES / name
            if not path.exists():
                continue
            d = gc.read_doc("research_plan", path)
            f = gc.check_general(d, set()) + gc.check_profile(d, BSF["parts"]["research_plan"], BSF)
            self.assertEqual({x.code for x in f}, {"placeholder"}, name)


if __name__ == "__main__":
    unittest.main()
