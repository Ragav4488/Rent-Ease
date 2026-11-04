"""Assemble the BloodConnect-style RentEase mini project report."""
from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent
OUT_DOCX = ROOT / "RentEase_Mini_Project_Report.docx"

# run as a plain script or as -m; Report2 is an implicit namespace package
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

# later sections are written by other agents; a missing one is skipped, not fatal
LAZY = [
    ("exp01", "Report2.content.exp01", "build"),
    ("exp02", "Report2.content.exp02", "build"),
    ("exp03", "Report2.content.exp03", "build"),
    ("exp04", "Report2.content.exp04", "build"),
    ("exp05", "Report2.content.exp05", "build"),
    ("exp06", "Report2.content.exp06", "build"),
    ("exp07", "Report2.content.exp07", "build"),
    ("exp08", "Report2.content.exp08", "build"),
    ("mini.build_intro", "Report2.content.mini", "build_intro"),
    ("mini.build_code", "Report2.content.mini", "build_code"),
    ("mini.build_output", "Report2.content.mini", "build_output"),
    ("backmatter.build_comparison", "Report2.content.backmatter", "build_comparison"),
    ("backmatter.build_limits", "Report2.content.backmatter", "build_limits"),
    ("backmatter.build_result", "Report2.content.backmatter", "build_result"),
]


def _call(doc, name, module, attr):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        print(f"SKIPPED {name} (not yet written)")
        return False
    except Exception as exc:                      # noqa: BLE001
        print(f"SKIPPED {name} ({type(exc).__name__}: {exc})")
        return False
    fn = getattr(mod, attr, None)
    if not callable(fn):
        print(f"SKIPPED {name} (no {attr}() in {module})")
        return False
    fn(doc)
    return True


def build():
    from Report2 import theme
    from Report2.content import front

    doc = Document()
    theme.setup(doc)
    theme.page_frame(doc.sections[0])
    theme.footer_page_numbers(doc.sections[0])

    # front matter uses roman numerals (i, ii, iii...), body restarts at 1
    front.build_cover(doc)
    _roman_section(doc)
    front.build_certificate(doc)
    front.build_toc(doc)
    front.build_figures_list(doc)
    front.build_abbreviations(doc)

    # ---- the mini-project report itself: chapters 1-5 ----
    # new section: arabic page numbering restarts at 1 for the body
    _body_section(doc, theme)
    from Report2.content import chapters
    done = []

    chapters.build_abstract(doc)
    chapters.build_introduction(doc)

    # Chapter 3 embeds the code listings that live in mini.py
    def _code_listings(d):
        from Report2.content import mini
        mini.build_code(d)

    chapters.build_implementation(doc, code_builder=_code_listings)
    chapters.build_outcome(doc)
    chapters.build_conclusion(doc)
    chapters.build_references(doc)

    # Laboratory-record appendix omitted for this edition: the brief is a
    # ~30-page mini-project report in the reference's structure. Set
    # INCLUDE_APPENDIX=1 in the environment to append the nine exercises.
    import os
    if os.environ.get("INCLUDE_APPENDIX") == "1":
        front.build_experiments_list(doc)
        front.build_rubrics(doc)
        for name, module, attr in LAZY:
            if _call(doc, name, module, attr):
                done.append(name)

    doc.save(OUT_DOCX)
    print(f"wrote {OUT_DOCX}  ({OUT_DOCX.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"rendered {len(done)}/{len(LAZY)} annexure sections")
    return OUT_DOCX


def _body_section(doc, theme):
    """Start a new section whose numbering restarts at arabic 1."""
    from docx.enum.section import WD_SECTION
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    new = doc.add_section(WD_SECTION.NEW_PAGE)
    theme.page_frame(new)
    theme.footer_page_numbers(new)
    pg = new._sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        new._sectPr.insert_element_before(
            pg, "w:cols", "w:formProt", "w:vAlign", "w:noEndnote",
            "w:titlePg", "w:textDirection", "w:bidi", "w:rtlGutter",
            "w:docGrid", "w:printerSettings")
    pg.set(qn("w:fmt"), "decimal")
    pg.set(qn("w:start"), "1")


def _roman_section(doc):
    """Mark the current section footer as lower-roman, starting at i."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    sect = doc.sections[0]
    sect_pr = sect._sectPr
    pg = sect_pr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        sect_pr.insert_element_before(
            pg, "w:cols", "w:formProt", "w:vAlign", "w:noEndnote",
            "w:titlePg", "w:textDirection", "w:bidi", "w:rtlGutter",
            "w:docGrid", "w:printerSettings")
    pg.set(qn("w:fmt"), "lowerRoman")
    pg.set(qn("w:start"), "1")

def to_pdf(docx_path):
    profile = "file:///tmp/lo-profile-rentease2"
    subprocess.run([
        "soffice", "--headless",
        f"-env:UserInstallation={profile}",
        "--convert-to", "pdf", "--outdir", str(ROOT), str(docx_path),
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
    pdf = docx_path.with_suffix(".pdf")
    print(f"wrote {pdf}  ({pdf.stat().st_size / 1024 / 1024:.2f} MB)")
    return pdf


if __name__ == "__main__":
    path = build()
    if "--pdf" in sys.argv:
        to_pdf(path)
