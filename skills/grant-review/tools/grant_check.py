#!/usr/bin/env python3
"""Mechanical checks for a grant proposal draft, for any funder with a profile.

The funder-independent rules (placeholders, vague challenge statements,
deliverable-shaped objectives, hidden causality, passive voice, filler) are
built in and cite proposal_craft.md. Everything that belongs to one call --
which files exist, their length limits, required headings and content, font
and spacing rules, extra patterns -- comes from a JSON profile in profiles/,
and cites that funder's guide. A new funder is a new profile, not new code.

Findings are triaged:

  BLOCK   compliance, missing required content, or placeholder -- not submittable
  SCORE   weakens the answer to a named evaluation criterion
  POLISH  sentence-level; fix in a word pass

Judgment calls (is this objective a knowledge claim? is the collaboration
real?) are deliberately NOT here -- the review skills do those, and this
script exists so that they never spend attention on what a regex can settle.

Reads .tex, .md, .txt and .docx (stdlib only). For .docx, "line" means
paragraph number.

Usage:
    python3 grant_check.py --profile bsf                # parts found in the cwd
    python3 grant_check.py --profile bsf plan.docx      # one file, as part "research_plan"
    python3 grant_check.py --profile bsf --census       # what exists: parts, words, limits
    python3 grant_check.py --profile bsf --pages        # also count pages (see below)
    python3 grant_check.py --profile bsf --json         # machine-readable, for the skill
    python3 grant_check.py --list-profiles

Pages: .docx from the page count Word last saved; .tex by compiling with
tectonic if installed; .pdf directly. Text checks on a .pdf need pdftotext.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile
import zipfile
import zlib
from collections import Counter
from dataclasses import dataclass

TOOLS = pathlib.Path(__file__).resolve().parent
PROFILES = TOOLS / "profiles"
TEXT_SUFFIXES = (".tex", ".md", ".txt", ".docx", ".pdf")

# --- funder-independent patterns -------------------------------------------
# Each cites proposal_craft.md ("craft §n"), never a funder guide.

PLACEHOLDERS = [
    (r"HERE GOES", "unwritten placeholder text"),
    (r"X{4,}", "XXXX placeholder"),
    (r"DD/MM/YYYY|YYYY\s*--?\s*YYYY", "unfilled date template"),
    (r"Name Surname|\[(?:PI|Partner|Institution) ?[Nn]ame\]", "unfilled name template"),
    (r"%\s*EDIT:", "template EDIT marker still present"),
    (r"\\temp\{", r"\temp{} marker"),
    (r"\bTODO\b|\bFIXME\b|\bTBD\b", "TODO marker"),
    (r"\?\?\?", "??? marker"),
    (r"\[citation needed\]|\[cite\]|\[REF\]", "citation placeholder"),
    (r"\[\[[^\]]*\]\]", "unfilled template slot [[...]]"),
]

# "X is poorly understood" -- unscoreable challenge statements. craft §2.3.
VAGUE_CHALLENGE = [
    r"poorly understood",
    r"not (?:yet )?fully understood",
    r"not well understood",
    r"remains? (?:unclear|elusive|poorly|largely unknown|an open question)",
    r"(?:is|are) unclear",
    r"little is known",
    r"has received (?:limited|little) attention",
    r"despite (?:decades|years) of",
    r"has (?:not )?been (?:widely |extensively )?studied",
]

# craft §10, word level. Helper verbs and empty intensifiers.
FILLER = [
    r"\bsimply\b", r"\bclearly\b", r"\btrivially\b", r"\beasily\b",
    r"\bleverag(?:e|es|ed|ing)\b", r"\butiliz(?:e|es|ed|ing)\b",
    r"\bvery\b", r"\bextremely\b", r"\bquite\b", r"\bvarious\b",
    r"\bdifferent aspects\b",
]

# craft §10. Causal chains hidden behind and/then.
CAUSAL_SMELL = [
    (r"\band then\b", '"and then" -- name the causal relation'),
    (r"(?<![.!?])\.\s+Then\b", 'sentence opening with "Then"'),
    (r"\band we will\b.*\band we will\b", 'two "and we will" clauses in one sentence'),
]

# [\w-]+ed so hyphenated participles ("will be re-analysed") are caught too.
PASSIVE_FUTURE = r"\bwill be (?:[\w-]+ed|measured|shown|performed|conducted|investigated|analysed|analyzed)\b"

# An objective's label, however it is marked up: "\\textbf{Objective 1:}", "**Aim 2:**",
# "Specific Aim 1.2", "Problem III", "RQ1", "O1." -- but not "O2 release", which is chemistry.
OBJ_WORD = r"(?:Specific\s+)?(?:Objective|Aim|Goal|Problem|Research\s+question|RQ|Thrust|WP|Work\s+package)"
OBJ_LABEL = (r"^\s*(?:\\item\s*)?[#*_\s-]*(?:\\[a-z]+\{)?"
             r"(?:" + OBJ_WORD + r"\s*(?:\d+(?:\.\d+)?|(?-i:[IVX]+)\b)|OBJ\s*\d|(?-i:O\d)(?=[.:)]))"
             r"[.):]?\}?[*_\s]*:?[*_\s]*")

# Objectives should be knowledge claims, not deliverables. craft §4.
DELIVERABLE_VERBS = OBJ_LABEL + (r"(?:We will |To )?(?:Build|Implement|Release|Create|Deliver|"
                                 r"Produce|Set up|Develop a (?:tool|platform|database))\b")

# ...and checkable ones: nothing about "understand" or "study" can be met or missed. craft §4.
OPEN_VERBS = OBJ_LABEL + r"(?:We will |To )?(?:better )?(?:understand|study|investigate)\b"

BODY_NOTE_MAX_WORDS = 6

# --- model -------------------------------------------------------------------


@dataclass
class Finding:
    severity: str
    code: str
    file: str
    line: int
    message: str
    rule: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}  [{self.code}] {self.message}  ({self.rule})"


SEV_ORDER = {"BLOCK": 0, "SCORE": 1, "POLISH": 2}


@dataclass
class Doc:
    """One part of the proposal, reduced to numbered lines of text."""
    part: str
    path: pathlib.Path
    kind: str                      # tex | md | txt | docx | pdf
    lines: list[tuple[int, str]]   # comment-free, every line
    body: list[tuple[int, str]]    # lines that render as body text
    raw: str                       # full source text (comments included for tex)


# --- reading -----------------------------------------------------------------


def _strip_tex_comments(text: str) -> list[tuple[int, str]]:
    return [(i, re.sub(r"(?<!\\)%.*$", "", raw)) for i, raw in enumerate(text.splitlines(), 1)]


# Environments whose contents are drawing instructions, never prose.
DRAWING_ENVS = ("tikzpicture", "pgfpicture", "ganttchart", "axis", "tikzcd",
                "pspicture", "circuitikz")


def _tex_body(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    out, in_doc, in_draw = [], False, 0
    for n, line in lines:
        if r"\begin{document}" in line:
            in_doc = True
            continue
        if r"\end{document}" in line:
            break
        if not in_doc:
            continue
        for env in DRAWING_ENVS:
            in_draw += line.count(r"\begin{%s}" % env)
            in_draw -= line.count(r"\end{%s}" % env)
        if in_draw > 0 or any(r"\end{%s}" % e in line for e in DRAWING_ENVS):
            continue
        bare = line.strip()
        if not bare:
            continue
        if re.fullmatch(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})*\s*", bare):
            continue
        if re.fullmatch(r"\{*\\[a-zA-Z@]+\*?\}*", bare):
            continue
        out.append((n, bare))
    return out


def _docx_heading_levels(styles: str) -> dict[str, int]:
    """Style ID -> heading level. Built-in styles keep their English name ("heading 2") in
    w:name even where a localized Word gives them another ID, so read the name, not the ID."""
    levels = {}
    for m in re.finditer(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', styles, re.S):
        name = re.search(r'<w:name w:val="([^"]+)"', m.group(2))
        name = name.group(1).lower() if name else ""
        lvl = re.fullmatch(r"heading (\d)", name)
        outline = re.search(r'<w:outlineLvl w:val="(\d)"', m.group(2))
        if lvl:
            levels[m.group(1)] = int(lvl.group(1))
        elif name == "title":
            levels[m.group(1)] = 1
        elif outline:
            levels[m.group(1)] = int(outline.group(1)) + 1
    return levels


def _docx_paragraphs(path: pathlib.Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        styles = (z.read("word/styles.xml").decode("utf-8", errors="replace")
                  if "word/styles.xml" in z.namelist() else "")
    levels = _docx_heading_levels(styles)
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        p = re.sub(r"<w:tab/>", "\t", p)
        p = re.sub(r"<w:br/>", " ", p)
        text = "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))
        text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                    .replace("&quot;", '"').replace("&apos;", "'"))
        # Headings are marked as Markdown ones, so structure checks treat both formats alike.
        st = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        lvl = levels.get(st.group(1)) if st else None
        if st and lvl is None:                   # no styles.xml entry: trust an English ID
            m = re.fullmatch(r"Heading\s*(\d)|(Title)", st.group(1))
            lvl = (int(m.group(1)) if m.group(1) else 1) if m else None
        if lvl and text.strip():
            text = "#" * min(lvl, 6) + " " + text.strip()
        paras.append(text)
    return paras


def _pdf_text(path: pathlib.Path) -> str | None:
    if not _which("pdftotext"):
        return None
    r = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True)
    return None if r.returncode else r.stdout


def read_doc(part: str, path: pathlib.Path) -> Doc | None:
    kind = path.suffix.lower().lstrip(".")
    if kind == "docx":
        paras = _docx_paragraphs(path)
        lines = list(enumerate(paras, 1))
        raw = "\n".join(paras)
        body = [(n, t.strip()) for n, t in lines if t.strip()]
    elif kind == "pdf":
        raw = _pdf_text(path)
        if raw is None:
            return Doc(part, path, kind, [], [], "")
        lines = list(enumerate(raw.splitlines(), 1))
        body = [(n, t.strip()) for n, t in lines if t.strip()]
    else:
        raw = path.read_text(encoding="utf-8", errors="replace")
        if kind == "tex":
            lines = _strip_tex_comments(raw)
            body = _tex_body(lines)
            if not any(r"\begin{document}" in l for _, l in lines):
                body = [(n, l.strip()) for n, l in lines if l.strip()]   # an \input fragment
        else:
            # Comments are guidance, not text: blank them, keeping the line numbers.
            raw = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
            lines = list(enumerate(raw.splitlines(), 1))
            body = [(n, l.strip()) for n, l in lines
                    if l.strip() and not l.lstrip().startswith(("<!--", "```"))]
    return Doc(part, path, kind, lines, body, raw)


def content_lines(doc: Doc) -> list[tuple[int, str]]:
    """Every non-empty line of the document proper, headings included -- unlike
    doc.body, which drops lines that are a bare macro such as \\section{...}."""
    lines = doc.lines
    if doc.kind == "tex":
        start = next((i for i, (_, l) in enumerate(lines) if r"\begin{document}" in l), -1)
        lines = lines[start + 1:]
    return [(n, l.strip()) for n, l in lines if l.strip()]


def paragraphs(doc: Doc) -> list[tuple[int, str]]:
    """(first line, joined text) per paragraph, for patterns that span source lines."""
    if doc.kind in ("docx", "pdf"):
        return doc.body
    out, cur, first = [], [], 0
    body = dict(doc.body)
    for n, _ in content_lines(doc) + [(10**9, "")]:
        if n in body and (not cur or n == prev + 1):
            first = first if cur else n
            cur.append(body[n])
        else:
            if cur:
                out.append((first, " ".join(cur)))
            cur = [body[n]] if n in body else []
            first = n
        prev = n
    return out


def plain_text(doc: Doc) -> str:
    """Body text with markup removed, for word counts and sentence splitting."""
    text = "\n".join(l for _, l in doc.body)
    if doc.kind == "tex":
        text = re.sub(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", text)
        for _ in range(3):
            text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", text)
        text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
        text = re.sub(r"[{}$~]", " ", text)
    elif doc.kind == "md":
        text = re.sub(r"[#*_`>]+", " ", text)
    return text


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][\w'’-]*", text))


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]


# --- the funder-independent checks -------------------------------------------


def check_general(doc: Doc, disabled: set[str]) -> list[Finding]:
    f: list[Finding] = []
    name = doc.path.name

    def add(sev, code, line, msg, rule):
        if code not in disabled:
            f.append(Finding(sev, code, name, line, msg, rule))

    for n, line in doc.lines:
        for pat, desc in PLACEHOLDERS:
            if re.search(pat, line):
                add("BLOCK", "placeholder", n, desc, "craft §9")
        for _ in re.finditer(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{\s*\}", line):
            add("BLOCK", "empty-cite", n, "empty citation -- claim has no support", "craft §10")
        for _ in re.finditer(r"\\(?:ref|autoref|eqref|cref)\{\s*\}", line):
            add("BLOCK", "empty-ref", n, "empty cross-reference", "craft §9")

    for n, line in doc.body:
        for pat in VAGUE_CHALLENGE:
            m = re.search(pat, line, re.I)
            if m:
                add("SCORE", "vague-challenge", n,
                    f'"{m.group(0)}" -- say what specifically is unknown and why', "craft §2.3")
        if re.search(DELIVERABLE_VERBS, line, re.I):
            add("SCORE", "objective-deliverable", n,
                "objective opens with a build/deliver verb, not a knowledge verb", "craft §4")
        m = re.search(OPEN_VERBS, line, re.I)
        if m:
            add("SCORE", "objective-open-verb", n,
                f'"{m.group(0).strip()[:40]}" -- an open-ended verb cannot be met or missed; '
                "say what will be known", "craft §4")
        for pat, desc in CAUSAL_SMELL:
            if re.search(pat, line, re.I):
                add("SCORE", "causality", n, desc, "craft §10")
        for m in re.finditer(PASSIVE_FUTURE, line, re.I):
            add("POLISH", "passive", n, f'"{m.group(0)}" -- active voice, and say which team acts',
                "craft §10")
        for pat in FILLER:
            m = re.search(pat, line, re.I)
            if m:
                add("POLISH", "filler", n, f'filler: "{m.group(0)}"', "craft §10")

    if doc.kind == "tex":
        for n, line in doc.body:
            if line.startswith("\\") or line.endswith(("{", "}")) or "[[" in line or "]]" in line:
                continue
            if "&" in line or line.endswith("\\\\") or ":" in line:
                continue
            if re.search(r"\b(?:19|20)\d\d\b", line) or re.search(r"\\cite", line):
                continue
            if len(line.split()) <= BODY_NOTE_MAX_WORDS and not re.search(r"[.!?:]$", line):
                add("SCORE", "stray-note", n, f'note fragment renders as body text: "{line[:48]}"',
                    "craft §9")
    return f


# --- the profile-driven checks ------------------------------------------------


def check_profile(doc: Doc, spec: dict, profile: dict) -> list[Finding]:
    f: list[Finding] = []
    name = doc.path.name
    rule = spec.get("rule", profile["guide"])

    def add(sev, code, line, msg, r=rule):
        f.append(Finding(sev, code, name, line, msg, r))

    text = plain_text(doc)
    n_words = words(text)
    n_chars = len(re.sub(r"\s+", " ", text).strip())

    # Length limits that a source file can settle. Pages need --pages.
    wl = spec.get("word_limit")
    if wl and n_words > wl:
        # A hard cap blocks; "about N words" in the call is a SCORE in the profile.
        add(spec.get("word_limit_severity", "BLOCK"), "over-words", 1,
            f"{doc.part} is {n_words} words, limit {wl}")
    cl = spec.get("char_limit")
    if cl and n_chars > cl:
        add("BLOCK", "over-chars", 1, f"{doc.part} is {n_chars} characters, limit {cl}")
    floor = spec.get("word_floor")
    if floor and 0 < n_words < floor:
        add("SCORE", "thin", 1, f"{doc.part} is only {n_words} words of a {wl or floor}-word budget")

    # Required heading text, e.g. the BSF requires the word 'Abstract' in the abstract's heading.
    content = content_lines(doc)
    head = spec.get("required_heading")
    if head:
        top = " ".join(l for _, l in content[:12])
        if not re.search(re.escape(head), top, re.I):
            add("BLOCK", "heading-missing", 1, f"the word(s) '{head}' must appear in the heading")

    # Required content: every item must have an address, headings included. Absent means missing.
    # "within_words" confines the search to the opening, e.g. what must be on page 1.
    for item in spec.get("required_content", []):
        pats = item["any"]
        scope = (_opening(content, item["within_words"], item.get("until_heading"))
                 if item.get("within_words") else content)
        if item.get("headings_only"):
            scope = [(n, l) for n, l in scope if _is_heading(l)]
        hit = next(((n, l) for n, l in scope for p in pats if re.search(p, l, re.I)), None)
        if hit is None:
            add(item.get("severity", "BLOCK"), item["code"], 1, item["message"],
                item.get("rule", rule))

    if spec.get("task_owner"):
        f += check_task_owners(doc, spec)
    if spec.get("unit_requirements") or spec.get("max_objectives") or spec.get("proportions"):
        f += check_units(doc, spec, rule)

    # Format rules, settled from the source where the source says enough.
    fmt = spec.get("format")
    if fmt:
        f += check_format(doc, fmt)

    # Extra funder patterns.
    for p in profile.get("patterns", []):
        parts = p.get("parts")
        if parts and doc.part not in parts:
            continue
        flags = re.I if "i" in p.get("flags", "") else 0
        if p.get("scope") == "paragraph":
            src = paragraphs(doc)
        else:
            src = doc.body if p.get("body_only", True) else doc.lines
        for n, line in src:
            m = re.search(p["pattern"], line, flags)
            if m:
                msg = p["message"].replace("{match}", m.group(0))
                add(p["severity"], p["code"], n, msg, p.get("rule", profile["guide"]))
                if p.get("once"):
                    break
    return f


# Baselineskip of the standard LaTeX classes, by base font size (pt).
TEX_BASELINE = {10: 12.0, 11: 13.6, 12: 14.5}
# setspace's stretch factors, which are *not* 1.5 and 2.0 -- see check_format.
SETSPACE = {"onehalf": {10: 1.25, 11: 1.213, 12: 1.241}, "double": {10: 1.667, 11: 1.618, 12: 1.655}}
PAPER_HEIGHT_CM = {"a4": 29.7, "letter": 27.94}


def _len_cm(val: str) -> float | None:
    m = re.match(r"\s*([\d.]+)\s*(cm|mm|in|pt|bp)\s*$", val)
    if not m:
        return None
    x, unit = float(m.group(1)), m.group(2)
    return {"cm": x, "mm": x / 10, "in": x * 2.54, "pt": x * 2.54 / 72.27, "bp": x * 2.54 / 72}[unit]


def check_format(doc: Doc, fmt: dict) -> list[Finding]:
    f: list[Finding] = []
    rule = fmt.get("rule", "")
    name = doc.path.name

    def add(sev, code, line, msg):
        f.append(Finding(sev, code, name, line, msg, rule))

    if doc.kind == "tex":
        src = "\n".join(l for _, l in doc.lines)
        if r"\documentclass" not in src:
            return f                                   # a fragment; the main file decides
        line_of = lambda pat: next((n for n, l in doc.lines if re.search(pat, l)), 1)
        m = re.search(r"\\documentclass\[([^\]]*)\]", src)
        opts = m.group(1) if m else ""
        pt_m = re.search(r"(\d+)pt", opts)
        pt = int(pt_m.group(1)) if pt_m else 10
        if fmt.get("min_font_pt") and pt < fmt["min_font_pt"]:
            add("BLOCK", "font-small", line_of(r"\\documentclass"),
                f"body font is {pt}pt, minimum {fmt['min_font_pt']}pt")
        paper = "a4" if "a4paper" in opts else "letter"          # LaTeX's default is letter
        gm = re.search(r"\\(?:usepackage|geometry)(?:\[([^\]]*)\])?\{(?:geometry|([^}]*))\}", src)
        gopts = ",".join(g for g in (gm.groups() if gm else ()) if g) if gm else ""
        if "a4paper" in gopts:
            paper = "a4"
        elif "letterpaper" in gopts:
            paper = "letter"
        margins = {}
        for key in ("margin", "top", "bottom", "left", "right", "hmargin", "vmargin"):
            mm = re.search(rf"(?<![a-z]){key}\s*=\s*([\d.]+\s*[a-z]{{2}})", gopts)
            if mm and _len_cm(mm.group(1)) is not None:
                margins[key] = _len_cm(mm.group(1))
        side = {k: margins.get(k, margins.get("margin")) for k in ("top", "bottom", "left", "right")}
        if fmt.get("min_margin_cm"):
            if not gm:
                add("SCORE", "margin-unknown", 1,
                    "no geometry package: LaTeX's default margins are wide but unstated -- set them")
            for k, v in side.items():
                if v is not None and v < fmt["min_margin_cm"] - 1e-6:
                    add("BLOCK", "margin-small", line_of(r"geometry"),
                        f"{k} margin {v:.2f} cm, minimum {fmt['min_margin_cm']} cm")
        stretch, how = 1.0, "single"
        sm = re.search(r"\\(?:linespread|setstretch)\{([\d.]+)\}", src)
        if sm:
            stretch, how = float(sm.group(1)), sm.group(0)
        elif re.search(r"\\onehalfspacing|\\begin\{onehalfspace\}", src):
            stretch, how = SETSPACE["onehalf"].get(pt, 1.241), r"\onehalfspacing"
        elif re.search(r"\\doublespacing|\\begin\{doublespace\}", src):
            stretch, how = SETSPACE["double"].get(pt, 1.655), r"\doublespacing"
        if fmt.get("min_font_pt"):
            small = [n for n, l in doc.body
                     if re.search(r"\\(?:small|footnotesize|scriptsize|tiny)\b", l) and "caption" not in l]
            if small:
                add("SCORE", "font-small-runs", small[0],
                    f"\\small or smaller in {len(small)} place(s) outside captions -- smaller type is "
                    "allowed only for formulas, captions and symbols")
        if fmt.get("min_line_spacing") and how == "single":
            add("BLOCK", "spacing-single", 1,
                f"single line spacing; at least {fmt['min_line_spacing']} required")
        # The trap: setspace's \onehalfspacing is 1.5 "typographically", i.e. a stretch of
        # ~1.24, so at 12pt on A4 with 2 cm margins it fits ~40 lines -- over a 38-line cap.
        if fmt.get("max_lines_per_page") and paper and side["top"] and side["bottom"]:
            text_h_pt = (PAPER_HEIGHT_CM[paper] - side["top"] - side["bottom"]) / 2.54 * 72.27
            skip = TEX_BASELINE.get(pt, 1.2 * pt) * stretch
            n_lines = math.floor((text_h_pt - pt) / skip) + 1
            if n_lines > fmt["max_lines_per_page"]:
                add("BLOCK", "lines-per-page", line_of(r"spacing|linespread|setstretch|geometry"),
                    f"{how} at {pt}pt on {paper} gives ~{n_lines} lines/page, cap "
                    f"{fmt['max_lines_per_page']} -- use \\linespread{{1.5}} or a taller margin")
        elif fmt.get("max_lines_per_page"):
            add("POLISH", "lines-unknown", 1,
                "lines per page not settled from source (paper size or margins unstated); "
                "count them on the compiled PDF")
    elif doc.kind == "docx":
        f += _check_docx_format(doc, fmt, add)
    return f


def _check_docx_format(doc: Doc, fmt: dict, add) -> list[Finding]:
    with zipfile.ZipFile(doc.path) as z:
        styles = z.read("word/styles.xml").decode("utf-8", "replace") if "word/styles.xml" in z.namelist() else ""
        body = z.read("word/document.xml").decode("utf-8", "replace")
    normal = re.search(r'<w:style [^>]*w:styleId="Normal".*?</w:style>', styles, re.S)
    defaults = re.search(r"<w:docDefaults>.*?</w:docDefaults>", styles, re.S)
    scope = (normal.group(0) if normal else "") + (defaults.group(0) if defaults else "")
    sz = re.search(r'<w:sz w:val="(\d+)"', scope)
    if fmt.get("min_font_pt") and sz and int(sz.group(1)) / 2 < fmt["min_font_pt"]:
        add("BLOCK", "font-small", 1,
            f"Normal style is {int(sz.group(1)) / 2:g}pt, minimum {fmt['min_font_pt']}pt")
    sizes = [int(s) / 2 for s in re.findall(r'<w:sz w:val="(\d+)"', body)]
    small = [s for s in sizes if fmt.get("min_font_pt") and s < fmt["min_font_pt"]]
    if small:
        add("SCORE", "font-small-runs", 1,
            f"{len(small)} text runs below {fmt['min_font_pt']}pt (smallest {min(small):g}pt) -- "
            "allowed only for formulas, captions and symbols")
    sp = re.search(r'<w:spacing [^>]*w:line="(\d+)"(?: [^>]*w:lineRule="(\w+)")?', scope)
    if fmt.get("min_line_spacing"):
        if sp and (sp.group(2) in (None, "auto")):
            factor = int(sp.group(1)) / 240
            if factor < fmt["min_line_spacing"] - 1e-6:
                add("BLOCK", "spacing-single", 1,
                    f"Normal style line spacing {factor:g}, minimum {fmt['min_line_spacing']}")
        elif not sp:
            add("BLOCK", "spacing-single", 1, "Normal style has no line spacing set (single)")
    pg = re.search(r"<w:pgMar ([^>]*)/>", body)
    if fmt.get("min_margin_cm") and pg:
        for side in ("top", "bottom", "left", "right"):
            v = re.search(rf'w:{side}="(\d+)"', pg.group(1))
            if v and int(v.group(1)) / 1440 * 2.54 < fmt["min_margin_cm"] - 1e-6:
                add("BLOCK", "margin-small", 1,
                    f"{side} margin {int(v.group(1)) / 1440 * 2.54:.2f} cm, minimum {fmt['min_margin_cm']} cm")
    return []


# --- structure, census, pages -------------------------------------------------


DEPTH = {"section": 0, "subsection": 1, "subsubsection": 2, "paragraph": 3}


def structure_units(doc: Doc, with_text: bool = False) -> list[dict]:
    """Every heading with its length, and any shape flag. craft §9.3, §9.4."""
    if doc.kind == "tex":
        src = re.sub(r"(?<!\\)%.*", "", doc.raw)
        head_re = re.compile(r"\\((?:sub)*section|paragraph)(\*?)\{([^}]*)\}")
        marks = [(m.start(), m.end(), m.group(1), m.group(3), m.group(2)) for m in head_re.finditer(src)]
        starts = [st for st, _, _, _, _ in marks]
        chunks = [src[e: (marks[i + 1][0] if i + 1 < len(marks) else len(src))]
                  for i, (_, e, _, _, _) in enumerate(marks)]
        kinds = [k for _, _, k, _, _ in marks]
        titles = [t for _, _, _, t, _ in marks]
        # A starred heading with nothing under it, e.g. \section*{Research Plan}, is a title.
        titles_only = {i for i, (_, _, _, _, star) in enumerate(marks) if star}
    elif doc.kind in ("md", "docx"):
        src = doc.raw
        heads = list(re.finditer(r"(?m)^(#{1,6})\s+(.*)$", src))
        hashes = [len(m.group(1)) for m in heads]
        # A lone top-level heading ("# Research Plan") is the title; the levels below it are
        # ranked, so "#" items with "##" aims read the same as "##" items with "###" aims.
        lone_title = bool(hashes) and hashes.count(min(hashes)) == 1 and hashes[0] == min(hashes)
        used = sorted(set(hashes[1:] if lone_title else hashes))
        rank = {h: ("section", "subsection", "subsubsection", "paragraph")[min(i, 3)]
                for i, h in enumerate(used)}
        kinds = ["section" if (lone_title and i == 0) else rank[h] for i, h in enumerate(hashes)]
        titles = [m.group(2).strip() for m in heads]
        starts = [m.start() for m in heads]
        chunks = [src[m.end(): (heads[i + 1].start() if i + 1 < len(heads) else len(src))]
                  for i, m in enumerate(heads)]
        titles_only = {0} if lone_title else set()
    else:
        return []
    out = []
    for i, (kind, title, chunk) in enumerate(zip(kinds, titles, chunks)):
        chunk = re.sub(r"\\end\{document\}.*", "", chunk, flags=re.S)
        text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", chunk)
        sents = sentences(text)
        n = words(text)
        # A task is named as one; a run-in \paragraph{Significance.} is only a heading.
        is_task = re.match(r"(?i)(?:task|T)\s*\d|task\b|moonshot", title)
        clean_tail = i + 1 < len(kinds) and kinds[i + 1] == kind
        # A heading followed directly by a deeper one is a container, not an empty unit.
        container = i + 1 < len(kinds) and DEPTH[kinds[i + 1]] > DEPTH[kind]
        note = ""
        if n == 0 and not container and i not in titles_only:
            note = "unwritten"
        elif is_task:
            moon = "moonshot" in title.lower()
            if moon and n > 260:
                note = "moonshot over ~200 words (craft §9.4)"
            elif not moon and len(sents) < 6:
                note = "task under purpose+approach+contribution length (craft §9.3)"
            elif not moon and len(sents) > 14 and clean_tail:
                note = "task longer than 4-8 approach sentences implies (craft §9.3)"
        unit = {"file": doc.path.name, "kind": kind, "title": title.strip(),
                "words": n, "sentences": len(sents), "flag": note}
        if with_text:
            unit.update(text=text, src=_unwrap(chunk), is_task=bool(is_task),
                        line=src.count("\n", 0, starts[i]) + 1)
        out.append(unit)
    return out


def check_task_owners(doc: Doc, spec: dict) -> list[Finding]:
    """Every task names the group that leads it. A multi-site plan where tasks
    name no group reads as one lab's plan with a partner attached."""
    own = spec["task_owner"]
    out = []
    for u in structure_units(doc, with_text=True):
        if not u["is_task"] or u["words"] < 15:
            continue
        if not any(re.search(p, u["title"] + " " + u["text"], re.I) for p in own["any"]):
            out.append(Finding(own.get("severity", "SCORE"), "task-owner", doc.path.name, u["line"],
                               f'task "{u["title"][:40]}" names no lead group or site', own["rule"]))
    return out


def _unwrap(src: str) -> str:
    """Markup removed but macro arguments kept, so \\textbf{O1. Determine ...} still reads."""
    src = re.sub(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", src)
    for _ in range(3):
        src = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", src)
    return re.sub(r"\\[a-zA-Z]+\*?|[{}$~]", " ", src)


def _is_heading(line: str) -> bool:
    return bool(re.match(r"\\(?:(?:sub)*section|paragraph)\*?\{|#+ ", line))


def _opening(content: list[tuple[int, str]], n_words: int,
             until: str | None = None) -> list[tuple[int, str]]:
    """The first n_words of content, stopping early at a heading that matches `until`."""
    out, total = [], 0
    for n, l in content:
        if until and _is_heading(l) and re.search(until, l, re.I):
            break
        out.append((n, l))
        if not re.fullmatch(r"\\[a-zA-Z]+\*?(\{[^{}]*\})*|#+ .*", l):
            total += words(re.sub(r"\\[a-zA-Z]+\*?", " ", l))
        if total >= n_words:
            break
    return out


def _subtrees(units: list[dict]) -> list[str]:
    """Each unit's own text plus that of every heading nested under it."""
    out = []
    for i, u in enumerate(units):
        texts = [u["src"]]
        for v in units[i + 1:]:
            if DEPTH[v["kind"]] <= DEPTH[u["kind"]]:
                break
            texts.append(v["title"] + " " + v["src"])
        out.append(" ".join(texts))
    return out


def check_units(doc: Doc, spec: dict, rule: str) -> list[Finding]:
    """Shape rules over headings: what every objective block must contain, how many
    objectives there are, and which sections must outweigh which."""
    out: list[Finding] = []
    units = structure_units(doc, with_text=True)
    trees = _subtrees(units)
    name = doc.path.name
    # The level the funder's items sit at: the shallowest with two headings naming an item.
    # A numbered \section{Research Plan} with the items as \subsection is then read correctly.
    items = spec.get("item_headings")
    depths = sorted({DEPTH[u["kind"]] for u in units})
    level = next((d for d in depths if items and sum(
        1 for u in units if DEPTH[u["kind"]] == d and re.search(items, u["title"], re.I)) >= 2),
        depths[0] if depths else 0)
    item_of, current = [], None                 # each unit's enclosing item heading
    for u in units:
        if DEPTH[u["kind"]] == level:
            current = u["title"]
        item_of.append(current if DEPTH[u["kind"]] >= level else None)

    # Every unit whose heading matches must contain one of the patterns, nested headings included.
    # "within" confines this to units under a matching item, e.g. the methodology, so objectives
    # restated in item 2 are not asked for item 3's success criteria.
    for req in spec.get("unit_requirements", []):
        inside = req.get("within")
        if inside and not any(t and re.search(inside, t, re.I) for t in item_of):
            inside = None                       # no such item heading: check every block
        for u, tree, it in zip(units, trees, item_of):
            if not re.search(req["title"], u["title"], re.I) or words(tree) < req.get("min_words", 40):
                continue
            if inside and not (it and re.search(inside, it, re.I)):
                continue
            if not any(re.search(p, u["title"] + " " + tree, re.I) for p in req["any"]):
                out.append(Finding(req.get("severity", "SCORE"), req["code"], name, u["line"],
                                   f'"{u["title"][:40]}": ' + req["message"], req.get("rule", rule)))

    # Objectives counted by their labels, wherever they are written.
    mo = spec.get("max_objectives")
    if mo:
        text = "\n".join(l for _, l in content_lines(doc))
        nums = {int(next(g for g in m.groups() if g)) for m in re.finditer(mo["pattern"], text, re.I)}
        if nums and max(nums) > mo["max"]:
            out.append(Finding(mo.get("severity", "SCORE"), "too-many-objectives", name, 1,
                               f"{max(nums)} objectives; {mo['message']}", mo.get("rule", rule)))

    # Section weight, at the item level: sections matching "a" together outweigh those matching "b".
    if units:
        tops = [(u["title"], words(t)) for u, t in zip(units, trees) if DEPTH[u["kind"]] == level]
        for p in spec.get("proportions", []):
            a = sum(w for t, w in tops if re.search(p["a"], t, re.I))
            b = sum(w for t, w in tops if re.search(p["b"], t, re.I))
            if not (a and b):
                out.append(Finding("POLISH", p["code"] + "-unknown", name, 1,
                                   "section weight not checked: no heading matched " +
                                   ("the methodology" if not a else "the background or objectives"),
                                   p.get("rule", rule)))
            elif a < p.get("ratio", 1.0) * b:
                out.append(Finding(p.get("severity", "SCORE"), p["code"], name, 1,
                                   f"{a} words against {b} -- " + p["message"], p.get("rule", rule)))
    return out


def _which(prog: str) -> bool:
    return subprocess.run(["which", prog], capture_output=True).returncode == 0


def _pdf_pages(data: bytes) -> int:
    n = len(re.findall(rb"/Type\s*/Page\b(?!s)", data))
    if n:
        return n
    total = 0                                   # pages hidden in compressed object streams
    for m in re.finditer(rb"stream\r?\n", data):
        e = data.find(b"endstream", m.end())
        try:
            total += len(re.findall(rb"/Type\s*/Page\b(?!s)", zlib.decompress(data[m.end():e])))
        except Exception:
            continue
    return total


def page_count(doc: Doc) -> dict | None:
    """Pages and where the number came from, or None if it cannot be had."""
    if doc.kind == "pdf":
        return {"pages": _pdf_pages(doc.path.read_bytes()), "source": "pdf"}
    if doc.kind == "docx":
        with zipfile.ZipFile(doc.path) as z:
            if "docProps/app.xml" in z.namelist():
                m = re.search(r"<Pages>(\d+)</Pages>", z.read("docProps/app.xml").decode("utf-8", "replace"))
                if m:
                    return {"pages": int(m.group(1)), "source": "as last saved by Word"}
        return None
    if doc.kind == "tex" and _which("tectonic") and r"\documentclass" in doc.raw:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["tectonic", "-X", "compile", str(doc.path), "--outdir", tmp],
                           capture_output=True, cwd=doc.path.parent)
            pdf = pathlib.Path(tmp) / (doc.path.stem + ".pdf")
            if pdf.exists():
                return {"pages": _pdf_pages(pdf.read_bytes()), "source": "compiled"}
    sibling = doc.path.with_suffix(".pdf")
    if sibling.exists() and doc.kind != "pdf":
        return {"pages": _pdf_pages(sibling.read_bytes()), "source": f"{sibling.name} beside it"}
    return None


# --- profiles and targets -------------------------------------------------------


def load_profile(name: str) -> dict:
    p = pathlib.Path(name)
    path = p if p.suffix == ".json" and p.exists() else PROFILES / f"{name}.json"
    if not path.exists():
        sys.exit(f"no profile '{name}' -- try --list-profiles")
    return json.loads(path.read_text(encoding="utf-8"))


def _stem_matches(path: pathlib.Path, stems: list[str]) -> bool:
    s = path.stem.lower().replace("-", "_").replace(" ", "_")
    return any(s == st or s.startswith(st + "_") or s.endswith("_" + st) for st in stems)


def resolve(profile: dict, names: list[str]) -> list[Doc]:
    """Map files to the profile's parts by filename stem; an unmatched file is the main part."""
    parts = profile["parts"]
    main = profile.get("main_part", next(iter(parts)))
    if names:
        candidates = []
        for n in names:
            p = pathlib.Path(n)
            if p.is_dir():
                candidates += sorted(q for q in p.iterdir() if q.suffix.lower() in TEXT_SUFFIXES)
            elif p.exists():
                candidates.append(p)
            else:
                print(f"missing: {p}", file=sys.stderr)
        explicit = [p for p in names if pathlib.Path(p).is_file()]
    else:
        candidates = sorted(q for q in pathlib.Path.cwd().iterdir() if q.suffix.lower() in TEXT_SUFFIXES)
        explicit = []
    docs, taken = [], set()
    for part, spec in parts.items():
        stems = [s.lower() for s in spec.get("stems", [part])]
        # Prefer an editable source over a PDF of the same part.
        hits = sorted((c for c in candidates if _stem_matches(c, stems)),
                      key=lambda c: TEXT_SUFFIXES.index(c.suffix.lower()))
        if hits:
            docs.append(read_doc(part, hits[0]))
            taken.add(hits[0])
    for c in candidates:
        if c not in taken and str(c) in explicit:
            docs.append(read_doc(main, c))
    return [d for d in docs if d is not None]


def census(docs: list[Doc], profile: dict, want_pages: bool) -> dict:
    out = {"profile": profile["name"], "parts": {}, "missing": []}
    present = {d.part for d in docs}
    for part, spec in profile["parts"].items():
        if part not in present and spec.get("required", True):
            out["missing"].append(part)
    for d in docs:
        spec = profile["parts"][d.part]
        units = structure_units(d)
        out["parts"][d.part] = {
            "file": d.path.name,
            "words": words(plain_text(d)),
            "word_limit": spec.get("word_limit"),
            "page_limit": spec.get("page_limit"),
            "pages": page_count(d) if want_pages else None,
            "unwritten": [u["title"] for u in units if u["words"] == 0],
            "placeholders": sum(1 for f in check_general(d, set()) if f.code == "placeholder"),
            "shape_flags": [{"title": u["title"], "flag": u["flag"]}
                            for u in units if u["flag"] and u["flag"] != "unwritten"],
        }
    return out


# --- main -------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--profile", default="generic", help="funder profile name or path to .json")
    ap.add_argument("--pages", action="store_true", help="also count pages")
    ap.add_argument("--only", choices=["BLOCK", "SCORE", "POLISH"])
    ap.add_argument("--census", action="store_true", help="what exists: parts, words, limits")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list-profiles", action="store_true")
    args = ap.parse_args()

    if args.list_profiles:
        for p in sorted(PROFILES.glob("*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            print(f"{p.stem:<10} {d['name']}  (verified {d.get('verified', 'n/a')})")
        return 0

    profile = load_profile(args.profile)
    docs = resolve(profile, args.files)
    if not docs:
        stems = "; ".join(f"{k}: {', '.join(v.get('stems', [k]))}" for k, v in profile["parts"].items())
        print(f"no proposal parts found for profile '{args.profile}'. Expected filename stems -- "
              f"{stems} -- in .tex/.md/.txt/.docx/.pdf, or name the files.", file=sys.stderr)
        return 2
    unreadable = [d for d in docs if d.kind == "pdf" and not d.raw]
    for d in unreadable:
        print(f"note: {d.path.name} is a PDF and pdftotext is not installed -- "
              "only its page count is checked", file=sys.stderr)

    if args.census:
        data = census(docs, profile, args.pages)
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return 0
        print(f"profile: {data['profile']}")
        for part, p in data["parts"].items():
            lim = []
            if p["word_limit"]:
                lim.append(f"{p['words']} of {p['word_limit']} words")
            else:
                lim.append(f"{p['words']} words")
            if p["pages"]:
                lim.append(f"{p['pages']['pages']} of {p['page_limit'] or '?'} pages ({p['pages']['source']})")
            elif p["page_limit"]:
                lim.append(f"page limit {p['page_limit']} (not counted; --pages)")
            print(f"{part} [{p['file']}]: " + ", ".join(lim))
            if p["unwritten"]:
                print(f"  unwritten ({len(p['unwritten'])}): " + "; ".join(p["unwritten"][:8]))
            if p["placeholders"]:
                print(f"  placeholder text in {p['placeholders']} place(s)")
            for s in p["shape_flags"]:
                print(f"  {s['title'][:48]:<50} {s['flag']}")
        if data["missing"]:
            print("not found: " + ", ".join(data["missing"]))
        return 0

    disabled = set(profile.get("disable", []))
    findings: list[Finding] = []
    for d in docs:
        findings += check_general(d, disabled)
        findings += check_profile(d, profile["parts"][d.part], profile)
    present = {d.part for d in docs}
    if not args.files:
        for part, spec in profile["parts"].items():
            if part not in present and spec.get("required", True):
                findings.append(Finding("BLOCK", "part-missing", "-", 0,
                                        f"required part '{part}' not found "
                                        f"(stems: {', '.join(spec.get('stems', [part]))})",
                                        spec.get("rule", profile["guide"])))
    if args.only:
        findings = [f for f in findings if f.severity == args.only]
    findings.sort(key=lambda f: (SEV_ORDER[f.severity], f.file, f.line))
    counts = Counter(f.severity for f in findings)

    pages = {}
    if args.pages:
        for d in docs:
            pc = page_count(d)
            limit = profile["parts"][d.part].get("page_limit")
            pages[d.part] = {"count": pc, "limit": limit}
            if pc and limit and pc["pages"] > limit:
                f = Finding("BLOCK", "over-pages", d.path.name, 0,
                            f"{pc['pages']} pages ({pc['source']}), limit {limit}"
                            + ("; references included in this count" if profile["parts"][d.part].get("refs_excluded") else ""),
                            profile["parts"][d.part].get("rule", profile["guide"]))
                findings.insert(0, f)
                counts["BLOCK"] += 1

    if args.json:
        print(json.dumps({
            "profile": profile["name"],
            "findings": [vars(f) for f in findings],
            "structure": [u for d in docs for u in structure_units(d)],
            "pages": pages,
            "manual_checks": profile.get("manual_checks", []),
            "counts": dict(counts),
        }, indent=2, ensure_ascii=False))
        return 1 if counts["BLOCK"] else 0

    print(f"profile: {profile['name']}  (verified {profile.get('verified', 'n/a')})")
    for sev in ("BLOCK", "SCORE", "POLISH"):
        group = [f for f in findings if f.severity == sev]
        if group:
            print(f"\n=== {sev} ({len(group)}) ===")
            for f in group:
                print(" ", f)

    rows = [(d.path.name, structure_units(d)) for d in docs]
    if any(units for _, units in rows):
        print("\n=== STRUCTURE ===")
        for name, units in rows:
            if units:
                print(f" {name}")
            for u in units:
                print(f"  {u['kind']:<12} {u['title'][:52]:<54} {u['words']:>5}w {u['sentences']:>3}s"
                      + (f"  <- {u['flag']}" if u["flag"] else ""))

    if args.pages:
        print("\n=== PAGES ===")
        for part, p in pages.items():
            if p["count"] is None:
                print(f"  {part}: not counted (install tectonic, or put a PDF beside the source)")
            else:
                print(f"  {part}: {p['count']['pages']} pages"
                      + (f" of {p['limit']}" if p["limit"] else "") + f"  ({p['count']['source']})")

    if profile.get("manual_checks"):
        print("\n=== BY EYE (no script can check these) ===")
        for m in profile["manual_checks"]:
            print(f"  - {m}")

    print(f"\n{counts['BLOCK']} block, {counts['SCORE']} score, {counts['POLISH']} polish")
    return 1 if counts["BLOCK"] else 0


if __name__ == "__main__":
    sys.exit(main())
