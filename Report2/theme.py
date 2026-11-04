"""BloodConnect-style theme helpers for the RentEase lab record.

Typography and table styling are matched to /Users/sachin/Downloads/bloodconnect.pdf:

    body ............ Times New Roman 12 pt, justified, 1.5 spacing
    chapter head .... "CHAPTER - N" + TITLE, centred, bold 14 pt
    section head .... bold 12 pt
    tables .......... 11 pt, thin black borders, 0.85-grey (D9D9D9) header row
    captions ........ bold 12 pt, centred, "Fig 9.3  TITLE IN CAPS"
    page number ..... centred 10 pt, "- N -"
    margins ......... left 1.08", right 0.83", top/bottom 1.0"

Every helper takes the Document first so the content modules stay flat one-liners.
"""
from __future__ import annotations

from pathlib import Path

from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor, Emu

SERIF = "Times New Roman"
MONO = "Consolas"

BODY = Pt(12)
HEAD14 = Pt(14)
SMALL = Pt(11)
CODE = Pt(9)
PAGENO = Pt(10)

BLACK = RGBColor(0, 0, 0)
GREY_HDR = "D9D9D9"          # 0.85 grey, as used in the reference tables
GREY_ZEBRA = "F2F2F2"
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

MARGINS = dict(top=1.0, bottom=1.0, left=1.08, right=0.83)
TEXT_WIDTH = 6.35            # inches of usable width on A4 at those margins


# ---------------------------------------------------------------- low level
def _font(run, name=SERIF, size=BODY, bold=False, italic=False, color=BLACK):
    run.font.name = name
    run.font.size = size
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)
    return run


def setup(doc):
    """Apply the reference document's base style and page geometry."""
    normal = doc.styles["Normal"]
    normal.font.name = SERIF
    normal.font.size = BODY
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.5
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), SERIF)

    sec = doc.sections[0]
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(MARGINS["top"])
    sec.bottom_margin = Inches(MARGINS["bottom"])
    sec.left_margin = Inches(MARGINS["left"])
    sec.right_margin = Inches(MARGINS["right"])
    return sec


def page_field(paragraph, roman=False):
    """Insert a PAGE / ROMAN field wrapped in dashes:  - 1 -   or  - i -"""
    def field(name):
        run = paragraph.add_run()
        _font(run, size=PAGENO)
        fld_begin = OxmlElement("w:fldChar")
        fld_begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = f" {name} "
        fld_sep = OxmlElement("w:fldChar")
        fld_sep.set(qn("w:fldCharType"), "separate")
        txt = OxmlElement("w:t")
        txt.text = "1"
        fld_end = OxmlElement("w:fldChar")
        fld_end.set(qn("w:fldCharType"), "end")
        for el in (fld_begin, instr, fld_sep, txt, fld_end):
            run._r.append(el)

    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(0)
    _font(paragraph.add_run("- "), size=PAGENO)
    field("PAGE" if not roman else "SECTIONPAGES")
    _font(paragraph.add_run(" -"), size=PAGENO)


def page_frame(section, inset_pt=24):
    """Full-page single-rule border, 24 pt inside every edge (reference)."""
    sect_pr = section._sectPr
    old = sect_pr.find(qn("w:pgBorders"))
    if old is not None:
        sect_pr.remove(old)
    borders = OxmlElement("w:pgBorders")
    borders.set(qn("w:offsetFrom"), "page")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")          # 0.75 pt
        el.set(qn("w:space"), str(inset_pt))
        el.set(qn("w:color"), "000000")
        borders.append(el)
    # w:pgBorders sits after w:pgMar/w:paperSrc and before w:pgNumType
    sect_pr.insert_element_before(
        borders, "w:pgNumType", "w:pgNumType", "w:cols", "w:formProt",
        "w:vAlign", "w:noEndnote", "w:titlePg", "w:textDirection",
        "w:bidi", "w:rtlGutter", "w:docGrid", "w:printerSettings")


def footer_page_numbers(section, roman=False):
    """Centred '- N -' page number.

    Each field character must live in its own run; packing begin/instr/
    separate/end into a single run is invalid and makes the number vanish
    once the section numbering changes.
    """
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _font(p.add_run("- "), size=PAGENO)

    def _fld(kind):
        run = p.add_run()
        _font(run, size=PAGENO)
        if kind == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = " PAGE "
        elif kind == "text":
            el = OxmlElement("w:t")
            el.text = "1"
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        run._r.append(el)

    _fld("begin")
    _fld("instr")
    _fld("separate")
    _fld("text")
    _fld("end")
    _font(p.add_run(" -"), size=PAGENO)


# ------------------------------------------------------------------ blocks
def para(doc, text="", size=BODY, bold=False, italic=False, align=None,
         before=0, after=0, spacing=1.5, color=BLACK, indent=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = spacing
    if indent is not None:
        pf.left_indent = Inches(indent)
    if align is not None:
        p.alignment = align
    if text:
        _font(p.add_run(text), size=size, bold=bold, italic=italic, color=color)
    return p


def body(doc, text, justify=False, before=0, after=9, indent=None):
    # reference body copy is left-aligned (ragged right); justify=False default
    return para(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY if justify else None,
                before=before, after=after, indent=indent)


def rich(doc, parts, size=BODY, align=None, before=0, after=6, spacing=1.5,
         indent=None):
    """parts = [(text, bold, italic), ...]"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = spacing
    if indent is not None:
        pf.left_indent = Inches(indent)
    if align is not None:
        p.alignment = align
    for text, bold, italic in parts:
        _font(p.add_run(text), size=size, bold=bold, italic=italic)
    return p


def chapter(doc, number, title, before=0):
    """CHAPTER - N  /  TITLE  — both centred, bold, 14 pt as in the reference."""
    para(doc, f"CHAPTER - {number}", size=HEAD14, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, before=before, after=2, spacing=1.5)
    para(doc, title, size=HEAD14, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, after=12, spacing=1.5)


def section(doc, text, before=10, after=4):
    """2.1 Background and Need for the Project — bold 12 pt."""
    return para(doc, text, size=BODY, bold=True, before=before, after=after,
                spacing=1.5)


def subsection(doc, text, before=8, after=3):
    return para(doc, text, size=BODY, bold=True, before=before, after=after,
                spacing=1.5)


def page_break(doc):
    doc.add_page_break()


def heading_plain(doc, text, before=10, after=4, size=BODY):
    """Used for AIM: / PROCEDURE: labels in the experiment sections."""
    return para(doc, text, size=size, bold=True, before=before, after=after,
                spacing=1.5)


# ------------------------------------------------------------------- lists
def bullets(doc, items, size=BODY):
    for item in items:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(0.35)
        pf.first_line_indent = Inches(-0.2)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.5
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _font(p.add_run("•  "), size=size)
        _font(p.add_run(item), size=size)


def numbered(doc, items, size=BODY):
    for i, item in enumerate(items, 1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(0.38)
        pf.first_line_indent = Inches(-0.38)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.45
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _font(p.add_run(f"{i}.  "), size=size)
        _font(p.add_run(item), size=size)


# ------------------------------------------------------------------ tables
def _shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def _cell(cell, text, size=SMALL, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.alignment = align
    _font(p.add_run(str(text)), size=size, bold=bold)


_TBLPR_AFTER_BORDERS = (
    "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
    "w:tblCaption", "w:tblDescription", "w:tblPrChange",
)


def _set_borders(tbl, val, color, size):
    """Create/replace w:tblBorders at its schema-correct position."""
    tbl_pr = tbl._tbl.tblPr
    old = tbl_pr.find(qn("w:tblBorders"))
    if old is not None:
        tbl_pr.remove(old)

    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), val)
        el.set(qn("w:sz"), size)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tbl_pr.insert_element_before(borders, *_TBLPR_AFTER_BORDERS)


def _fix_layout(tbl):
    """Force fixed layout without creating a second w:tblLayout."""
    tbl_pr = tbl._tbl.tblPr
    existing = tbl_pr.findall(qn("w:tblLayout"))
    if existing:
        for extra in existing[1:]:
            tbl_pr.remove(extra)
        existing[0].set(qn("w:type"), "fixed")
    else:
        tbl_pr.get_or_add_tblLayout().set(qn("w:type"), "fixed")


def _no_split_row(row):
    """Add w:cantSplit once. Calling it twice must not duplicate the element:
    OOXML allows at most one w:cantSplit per w:trPr, and two writers (theme
    and a content module) can otherwise both add it."""
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:cantSplit")) is None:
        # w:cantSplit must be the FIRST child of w:trPr per the schema
        el = OxmlElement("w:cantSplit")
        tr_pr.insert(0, el)


def table(doc, rows, widths=None, caption=None, size=SMALL, header=True,
          align_center=False, zebra=False):
    """Thin black borders + 0.85-grey header, exactly like the reference tables."""
    if caption:
        caption_line(doc, caption)

    ncols = len(rows[0])
    t = doc.add_table(rows=len(rows), cols=ncols)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Hairline black rules. w:tblBorders must sit in schema order inside
    # w:tblPr (after w:tblInd, before w:shd/w:tblLayout/w:tblLook); appending
    # it at the end makes Word and LibreOffice silently drop the borders.
    _set_borders(t, "single", "000000", "4")

    for r, row in enumerate(rows):
        _no_split_row(t.rows[r])
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            is_head = header and r == 0
            _cell(cell, val, size=size, bold=is_head,
                  align=WD_ALIGN_PARAGRAPH.CENTER if (is_head or align_center)
                  else WD_ALIGN_PARAGRAPH.LEFT)  # body left-aligned per reference
            if is_head:
                _shade(cell, GREY_HDR)
            elif zebra and r % 2 == 0:
                _shade(cell, GREY_ZEBRA)

    if widths:
        t.autofit = False
        _fix_layout(t)
        grid = t._tbl.find(qn("w:tblGrid"))
        if grid is not None:
            for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
                gc.set(qn("w:w"), str(int(w * 1440)))
        for row in t.rows:
            for c, w in enumerate(widths):
                row.cells[c].width = Inches(w)

    # hairline spacer: a normal 12 pt paragraph here can spill onto a new
    # page when the table ends near the bottom margin, leaving a blank page.
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(0)
    sp.paragraph_format.line_spacing = Pt(1)
    sp.add_run("").font.size = Pt(1)
    return t


# ---------------------------------------------------------------- captions
def caption_line(doc, text, before=6, after=4):
    """Bold and centred. The label keeps its case; the title is upper-cased
    by callers, matching 'Table 3.3 CORE DATA ENTITIES'."""
    # keep the 'Fig 3.1' / 'Table 2.1' label as written; upper-case the title
    import re as _re
    m = _re.match(r"^(Fig\s+[\d.]+|Table\s+[\d.]+)\s*(.*)$", text, _re.I)
    if m:
        text = f"{m.group(1)}  {m.group(2).upper()}"
    return para(doc, text, size=BODY, bold=True,
                align=WD_ALIGN_PARAGRAPH.CENTER,
                before=before, after=after, spacing=1.0)


def figure(doc, path, caption, width_in=TEXT_WIDTH, max_h_in=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    pic = p.add_run().add_picture(str(path), width=Inches(width_in))
    if max_h_in:
        max_h = Inches(max_h_in)
        if pic.height > max_h:
            ratio = max_h / pic.height
            pic.width = Emu(int(pic.width * ratio))
            pic.height = Emu(int(pic.height * ratio))
    if caption:
        caption_line(doc, caption, before=2, after=8)


# -------------------------------------------------------------------- code
def code(doc, text, size=CODE):
    """Fixed-width listing with a light left rule."""
    lines = text.replace("\t", "    ").split("\n")
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.0
    pf.left_indent = Inches(0.1)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    ppr = p._p.get_or_add_pPr()
    pdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "12")
    left.set(qn("w:space"), "6")
    left.set(qn("w:color"), "BFBFBF")
    pdr.append(left)
    ppr.append(pdr)

    for i, line in enumerate(lines):
        run = p.add_run(line)
        _font(run, name=MONO, size=size, color=RGBColor(0x1A, 0x1A, 0x1A))
        if i < len(lines) - 1:
            run.add_break(WD_BREAK.LINE)
    return p


# --------------------------------------------------------- experiment block
def exp_head(doc, number, date, title):
    """ 'Ex No: 01        08/07/2026'  then the title, bold, left aligned."""
    rich(doc, [(f"Ex No: {number}", True, False), ("\t\t", False, False),
               (date, True, False)], after=6)
    para(doc, title, size=BODY, bold=True, after=4)


def rubric_table(doc, caption="Rubrics"):
    # keep the block compact so it does not straddle a page boundary
    caption_line(doc, caption, before=8, after=2)
    rows = [["Rubrics", "Actual Marks", "Awarded Marks"]]
    for name in ("Understanding (R1)", "Timeline (R2)", "Design (R3)",
                 "Development (R4)", "Innovation (R5)"):
        rows.append([name, "4", ""])
    rows.append(["Total Marks", "20", ""])
    t = table(doc, rows, widths=[3.0, 1.6, 1.6], size=Pt(10.5), align_center=True)
    for c in t.rows[-1].cells:
        for r in c.paragraphs[0].runs:
            r.font.bold = True
        _shade(c, GREY_HDR)

    # Word cannot keep a whole table on one page on its own. Marking every
    # row atomic still lets the LAST row spill and leaves an otherwise blank
    # page; setting keep_with_next on the caption + first rows holds the
    # block together.
    for row in t.rows[:-1]:
        for cell in row.cells:
            for par in cell.paragraphs:
                par.paragraph_format.keep_with_next = True
    return t


def table_borderless(doc, rows, widths=None, size=SMALL, align_center=False):
    """Same grid as table() but with no visible rules (certificate signatures)."""
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_borders(t, "none", "auto", "0")

    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            _cell(t.cell(r, c), val, size=size,
                  align=WD_ALIGN_PARAGRAPH.CENTER if align_center
                  else WD_ALIGN_PARAGRAPH.LEFT)

    if widths:
        t.autofit = False
        _fix_layout(t)
        grid = t._tbl.find(qn("w:tblGrid"))
        if grid is not None:
            for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
                gc.set(qn("w:w"), str(int(w * 1440)))
        for row in t.rows:
            for c, w in enumerate(widths):
                row.cells[c].width = Inches(w)
    return t
