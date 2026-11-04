"""Front matter: cover, certificate, contents, abbreviations, experiments, rubrics."""
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from .. import theme

FIG = Path(__file__).resolve().parent.parent / "figures"
CENTER = WD_ALIGN_PARAGRAPH.CENTER

STUDENT = "____________________________"

EXPERIMENTS = [
    ("1.", "Static web page design using HTML and CSS"),
    ("2.", "BMI Calculator using JavaScript"),
    ("3.", "User registration form validation using JavaScript"),
    ("4.", "Implementing web applications with API calls using JavaScript"),
    ("5.", "Event registration form using PHP and MySQL"),
    ("6.", "Web application for food delivery system using PHP and MySQL"),
    ("7.", "Web application for leave management using Servlet and MySQL"),
    ("8.", "Web application for online shopping using Servlet and MySQL"),
    ("9.", "Mini Project: RentEase - Rental Property Management System"),
]

CONTENTS = [
    ("", "LIST OF FIGURES", False, "iv"),
    ("", "LIST OF ABBREVIATIONS", False, "v"),
    ("1", "ABSTRACT", True, "1"),
    ("2", "INTRODUCTION", True, "2"),
    ("2.1", "Background and Need for the Project", False, "2"),
    ("2.2", "Objectives", False, "2"),
    ("2.3", "Scope", False, "3"),
    ("2.4", "Development Plan", False, "3"),
    ("3", "IMPLEMENTATION", True, "4"),
    ("3.1", "Tech Stack", False, "4"),
    ("3.2", "Modules", False, "5"),
    ("3.2.1", "Database Module", False, "5"),
    ("3.2.2", "Property Listing and Search Module", False, "6"),
    ("3.2.3", "Application and Payment Module", False, "6"),
    ("3.2.4", "Security and Interface Module", False, "7"),
    ("3.3", "Testing Approach", False, "7"),
    ("3.4", "Workflow of the Application", False, "8"),
    ("4", "OUTCOME", True, "11"),
    ("4.1", "Implementation Outcome", False, "11"),
    ("4.2", "Module-wise Outcome with Screenshots", False, "11"),
    ("4.3", "Comparison with Existing Methods", False, "19"),
    ("4.4", "Discussion and Limitations", False, "19"),
    ("5", "CONCLUSION", True, "21"),
    ("5.1", "Future Scope", False, "21"),
    ("", "REFERENCES", True, "22"),
]

ABBREVIATIONS = [
    ["API", "APPLICATION PROGRAMMING INTERFACE"],
    ["CSS", "CASCADING STYLE SHEETS"],
    ["CSRF", "CROSS-SITE REQUEST FORGERY"],
    ["DBMS", "DATABASE MANAGEMENT SYSTEM"],
    ["ER", "ENTITY RELATIONSHIP"],
    ["HTML", "HYPERTEXT MARKUP LANGUAGE"],
    ["HTTP", "HYPERTEXT TRANSFER PROTOCOL"],
    ["IDE", "INTEGRATED DEVELOPMENT ENVIRONMENT"],
    ["JSON", "JAVASCRIPT OBJECT NOTATION"],
    ["MYSQL", "MY STRUCTURED QUERY LANGUAGE"],
    ["OWASP", "OPEN WEB APPLICATION SECURITY PROJECT"],
    ["PDO", "PHP DATA OBJECTS"],
    ["PHP", "PHP: HYPERTEXT PREPROCESSOR"],
    ["REST", "REPRESENTATIONAL STATE TRANSFER"],
    ["SQL", "STRUCTURED QUERY LANGUAGE"],
    ["UI", "USER INTERFACE"],
    ["URL", "UNIFORM RESOURCE LOCATOR"],
    ["XAMPP", "CROSS-PLATFORM, APACHE, MARIADB, PHP AND PERL"],
    ["XSS", "CROSS-SITE SCRIPTING"],
]

RUBRICS = [
    ["Criteria / Points", "Strongly Acceptable (4)", "Acceptable (3)",
     "Considerable (2)", "Below Expectations (1)", "Unacceptable (0)"],
    ["Understanding the Problem Statement",
     "The procedure is explained and the problem is well designed with appropriate analysis",
     "Some programs are written accurately", "Major errors in program writing",
     "Programs are not written / wrong program written",
     "Programs are not written / wrong program written"],
    ["Completion of target in Lab", "100% target completed", "80% target completed",
     "70% target completed", "50% target completed", "25% target completed"],
    ["User Interface Design", "Well designed problem with appropriate analysis",
     "Designed the problem with analysis",
     "Missing some experimental procedure with partial analysis",
     "Missing major experimental details and analysis",
     "Could not explain the program"],
    ["Development / Implement", "Optimal solution with appropriate results",
     "80% of implementation done", "65% of implementation done",
     "Few procedures were explained", "No proper explanation on implementation"],
    ["Innovation", "Most of the innovations applied clearly",
     "Some of the innovations applied", "Few innovations applied clearly",
     "Innovations applied", "None of the innovations used"],
]


# ---------------------------------------------------------------- utilities
def _title(doc, text, size=theme.HEAD14):
    theme.para(doc, text, size=size, bold=True, align=CENTER, after=14,
               spacing=1.0)


def _stack(cell, lines):
    """Fill one table cell with one paragraph per line; the first two are bold."""
    for run in list(cell.paragraphs[0].runs):
        run._r.getparent().remove(run._r)
    for i, line in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(line)
        run.font.name = theme.SERIF
        run.font.size = theme.SMALL
        run.font.bold = i < 2


def _bold_row(row):
    for cell in row.cells:
        for run in cell.paragraphs[0].runs:
            run.font.bold = True


# ------------------------------------------------------------------- cover
def build_cover(doc):
    p = doc.add_paragraph()
    p.alignment = CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(str(FIG / "kpr_logo.jpg"), width=Inches(1.15))

    theme.para(doc, "KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY",
               size=Pt(12), bold=True, align=CENTER, before=4, spacing=1.0)
    theme.para(doc, "(Autonomous Institution)", size=Pt(10), bold=True,
               align=CENTER, spacing=1.0)

    theme.para(doc, "RENTEASE", size=Pt(18), bold=True, align=CENTER,
               before=50, after=8, spacing=1.0)
    theme.para(doc, "RENTAL PROPERTY MANAGEMENT SYSTEM", size=Pt(13), bold=True,
               align=CENTER, spacing=1.0)

    theme.para(doc, "A MINI PROJECT REPORT", size=Pt(13), bold=True,
               align=CENTER, before=64, after=10, spacing=1.0)
    theme.para(doc, "Submitted by", size=Pt(12), bold=True, italic=True,
               align=CENTER, before=4, spacing=1.0)
    theme.para(doc, STUDENT, size=Pt(12), bold=True, align=CENTER,
               before=4, after=16, spacing=1.0)

    theme.para(doc, "U21CS504 - Web Technologies Laboratory", size=Pt(12),
               bold=True, align=CENTER, before=12, spacing=1.0)
    theme.para(doc, "in", size=Pt(12), bold=True, italic=True, align=CENTER,
               before=12, spacing=1.0)
    theme.para(doc, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
               size=Pt(12), bold=True, align=CENTER, before=12, spacing=1.0)
    theme.para(doc, "KPRIET", size=Pt(12), bold=True, align=CENTER,
               spacing=1.0)

    theme.para(doc, "ARASUR, COIMBATORE - 641 407", size=Pt(12), bold=True,
               align=CENTER, before=118, spacing=1.0)
    theme.para(doc, "NOVEMBER 2026", size=Pt(12), bold=True, align=CENTER,
               before=6, spacing=1.0)
    theme.page_break(doc)


# ------------------------------------------------------------- certificate
def build_certificate(doc):
    _title(doc, "BONAFIDE CERTIFICATE")

    theme.rich(doc, [
        ("Certified that this project report ", False, False),
        ("\u201cRENTEASE \u2013 RENTAL PROPERTY MANAGEMENT SYSTEM\u201d", True, False),
        (" is the bonafide work of ", False, False),
        ("\u201c________________\u201d", True, False),
        (" who carried out the project work under my supervision.", False, False),
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=4, after=18)

    left = ["Dr. MIRUNA JOE AMALI", "HEAD OF THE DEPARTMENT", "Professor",
            "Computer Science and Engineering",
            "KPR Institute of Engineering and Technology",
            "Arasur, Coimbatore \u2013 641407"]
    right = ["RAJESHKUMAR S", "SUPERVISOR,", "Assistant Professor III",
             "Computer Science and Engineering",
             "KPR Institute of Engineering and Technology",
             "Arasur, Coimbatore \u2013 641407"]
    t = theme.table(doc, [["", ""]], widths=[3.18, 3.17], header=False,
                    size=theme.SMALL)
    _stack(t.cell(0, 0), left)
    _stack(t.cell(0, 1), right)

    theme.para(doc, "Submitted for the University Mini project Viva \u2013 Voce "
                    "held on ____________", bold=True, before=150, spacing=1.5)
    theme.para(doc, "", before=40, spacing=1.0)

    t = theme.table_borderless(doc, [["INTERNAL EXAMINER", "EXTERNAL EXAMINER"]],
                               widths=[3.18, 3.17], size=theme.BODY)
    _bold_row(t.rows[0])
    theme.page_break(doc)


# ------------------------------------------------------------------- toc
def build_toc(doc):
    _title(doc, "TABLE OF CONTENTS")

    rows = [["CHAPTER NO", "TITLE", "PAGE NO"]]
    rows += [[no, title, pg] for no, title, _, pg in CONTENTS]
    t = theme.table(doc, rows, widths=[1.2, 3.95, 1.2], size=theme.SMALL)
    for i, (_, _, is_chapter, _p) in enumerate(CONTENTS, 1):
        if is_chapter:
            for run in t.rows[i].cells[1].paragraphs[0].runs:
                run.font.bold = True
    theme.page_break(doc)


FIGURES = [
    ("3.1", "SYSTEM ARCHITECTURE OF RENTEASE"),
    ("3.2", "ENTITY RELATIONSHIP DIAGRAM OF THE DATABASE"),
    ("4.1", "HOME PAGE WITH QUICK SEARCH AND FEATURED LISTINGS"),
    ("4.2", "PROPERTY CATALOGUE WITH THE FILTER PANEL"),
    ("4.3", "FILTERED CATALOGUE - COIMBATORE, 2 BHK, UNDER RS.20,000"),
    ("4.4", "LISTING DETAIL WITH GALLERY AND APPLICATION PANEL"),
    ("4.5", "LOGIN PAGE"),
    ("4.6", "TENANT DASHBOARD"),
    ("4.7", "RENT RECORDING FORM"),
    ("4.8", "MAINTENANCE COMPLAINT FORM AND TIMELINE"),
    ("4.9", "OWNER DASHBOARD"),
    ("4.10", "ADD PROPERTY FORM"),
]


def build_figures_list(doc):
    _title(doc, "LIST OF FIGURES")
    rows = [["FIGURE NO", "FIGURE NAME", "PAGE NO"]]
    rows += [[no, name, ""] for no, name in FIGURES]
    theme.table(doc, rows, widths=[1.1, 4.35, 0.9], size=theme.SMALL)
    theme.page_break(doc)


# ---------------------------------------------------------- abbreviations
def build_abbreviations(doc):
    _title(doc, "LIST OF ABBREVIATIONS")
    theme.table(doc, ABBREVIATIONS, widths=[1.3, 5.05], header=False,
                size=theme.SMALL)
    theme.page_break(doc)


# ------------------------------------------------------------ experiments
def build_experiments_list(doc):
    _title(doc, "LIST OF EXPERIMENTS")
    rows = [["Expr. No.", "Name of the Experiments", "Page No.", "Marks (20)",
             "Faculty Sign"]]
    rows += [[n, name, "", "", ""] for n, name in EXPERIMENTS]
    theme.table(doc, rows, widths=[0.62, 3.28, 0.8, 0.85, 0.8], size=Pt(10))
    theme.page_break(doc)


# ---------------------------------------------------------------- rubrics
def build_rubrics(doc):
    _title(doc, "Rubrics for Laboratory Experiments")
    theme.table(doc, RUBRICS, widths=[1.12, 1.05, 1.03, 1.03, 1.05, 1.07],
                size=Pt(9))
    theme.page_break(doc)
