"""Chapters 1-5 of the RentEase mini project report.

These are the chapters the TABLE OF CONTENTS advertises. The Ex No: 01..09
sections in content/ are the laboratory record; this module supplies the
abstract, introduction, implementation, outcome and conclusion narrative that
makes the document a mini-project report rather than nine stapled exercises.
"""
import os
from pathlib import Path

from .. import theme

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
SHOTS = ROOT.parent / "screenshots"

from docx.enum.text import WD_ALIGN_PARAGRAPH


# ------------------------------------------------------------------ chapter 1
def build_abstract(doc):
    theme.chapter(doc, 1, "ABSTRACT")
    theme.body(doc,
        "RentEase is a rental property management system built for two audiences that "
        "rarely share a tool: property owners who need to keep a portfolio of lettings "
        "straight, and tenants who need to find one. The application is written in PHP 8 "
        "against MySQL 9, with the front end in semantic HTML5, a single CSS3 stylesheet "
        "and a small amount of vanilla JavaScript, and it is delivered as a set of pages "
        "that a browser requests rather than a single-page application.")
    theme.body(doc,
        "An owner registers, publishes a property with a photograph, rent, deposit, area, "
        "furnishing and availability date, and thereafter sees every listing they hold on "
        "one dashboard along with the applications it has attracted, the rent collected "
        "against it and the maintenance complaints its tenant has raised. A tenant "
        "registers, searches the catalogue by keyword, city, bedroom count, property type, "
        "furnishing and budget, applies for a property with an occupation and family size, "
        "records a monthly rent payment against a transaction reference once approved, and "
        "raises maintenance complaints that move from open to in-progress to resolved.")
    theme.body(doc,
        "The data layer is six InnoDB tables - users, properties, property_images, "
        "applications, payments and complaints - held together by foreign keys and by two "
        "unique constraints that carry real business meaning: one application per tenant "
        "per property, and one payment per tenant per property per month. Those keys turn "
        "duplicate submissions into a database error rather than a duplicated record. "
        "Approving an application runs inside a transaction that marks the property "
        "occupied and rejects the competing pending applications together, so a property "
        "cannot end up with two approved tenants.")
    theme.body(doc,
        "Security is applied throughout rather than bolted on. Every query that carries "
        "user input is a PDO prepared statement, every POST form carries a CSRF token "
        "compared with hash_equals(), every page that needs a role checks it before doing "
        "any work, every owner action re-verifies that the record belongs to the signed-in "
        "owner, and every value printed back into HTML passes through htmlspecialchars(). "
        "Passwords are stored with password_hash() and sessions are regenerated on login.")
    theme.body(doc,
        "The completed system was exercised against a live MySQL instance for all six "
        "features and fifteen recorded test cases, with screenshots in Chapter 4. RentEase "
        "demonstrates server-side scripting, relational modelling with constraints that "
        "enforce business rules, session-based authentication, transactional updates and a "
        "responsive interface built without a framework.")


# ------------------------------------------------------------------ chapter 2
def build_introduction(doc):
    theme.chapter(doc, 2, "INTRODUCTION")

    theme.section(doc, "2.1 Background and Need for the Project")
    theme.body(doc,
        "Renting a house in an Indian city is still largely a brokerage transaction. A "
        "tenant rings an agent, the agent rings an owner, and the same flat is quoted at "
        "three different rents to three callers. What matters - the real cost, when it is "
        "free, whether the deposit is refundable, who fixes the plumbing - lives in the "
        "agent's memory and a WhatsApp thread. The owner has no consolidated record of who "
        "paid this month or which repair is still open.")
    theme.body(doc,
        "The problems with this practice cluster into four kinds: discovery, records, "
        "responsibility and trust. They are summarised in Table 2.1. Each one is a "
        "bookkeeping failure rather than a hard technical problem, which is what makes it "
        "worth solving in software.")
    theme.table(doc, [
        ["Problem", "Description", "Impact"],
        ["Scattered listings",
         "Flats are advertised through individual brokers and forwarded messages.",
         "A tenant cannot compare the market in one place."],
        ["No application record",
         "Interest is expressed on the phone and nothing is written down.",
         "Neither side can reconstruct who applied for what, or when."],
        ["Informal rent trail",
         "The tenant holds a receipt; the owner holds a notebook.",
         "Monthly reconciliation is manual and disputes are hard to settle."],
        ["Untracked maintenance",
         "A repair request is a phone call that leaves no history.",
         "Repairs are forgotten and responsibility is disputed later."],
        ["Broker dependency",
         "Contact details sit with the middleman, not with either party.",
         "Both sides pay for an introduction they cannot verify."],
    ], widths=[1.25, 2.75, 2.35],
        caption="Table 2.1  Problems in the existing methods of renting")

    theme.body(doc,
        "Problem statement: how can a single web application let an owner publish and track "
        "a portfolio of lettings, and let a tenant search that portfolio, apply, pay and "
        "raise complaints, such that every one of those actions leaves a record both parties "
        "can read?", before=8)

    theme.section(doc, "2.2 Objectives")
    theme.bullets(doc, [
        "To build a searchable property catalogue carrying an image gallery and a full "
        "specification sheet for each listing.",
        "To let an owner publish a listing, and to let a tenant search by keyword, city, "
        "bedroom count, property type, furnishing and maximum rent.",
        "To record rental applications and give the owner an approve or reject decision "
        "that cannot admit two tenants to one property.",
        "To keep a month-by-month rent payment record that cannot record the same month "
        "twice for the same tenant and property.",
        "To track maintenance complaints through a fixed status path with an owner note.",
        "To give the owner one dashboard covering listings, applications, rent collected "
        "and open complaints.",
        "To enforce role-based access, CSRF protection and bound SQL parameters on every "
        "page that changes state.",
    ])

    theme.section(doc, "2.3 Scope")
    theme.body(doc,
        "The delivered system covers owner and tenant registration, the property catalogue "
        "with its six filters and four sort orders, the listing detail page with gallery and "
        "application form, the application decision, rent recording, complaint tracking and "
        "the owner dashboard. It is six database tables, eighteen PHP files, one stylesheet "
        "and one script, and it runs either under XAMPP or under PHP's built-in server.")
    theme.body(doc,
        "The current version deliberately does not include a payment gateway - rent is "
        "recorded and reconciled, not charged - nor an identity or title verification step, "
        "an administrator role, e-mail or SMS notification, image resizing or a CDN, full "
        "text search, or a GPS proximity search. It also omits listing edit and delete "
        "paths, password reset and login rate limiting. These are listed under Future Scope "
        "in Chapter 5 rather than presented as complete.")

    theme.section(doc, "2.4 Development Plan")
    theme.body(doc,
        "The work proceeded in six phases, each feeding the next (Table 2.2).")
    theme.table(doc, [
        ["S.No", "Phase", "Activities", "Output"],
        ["1", "Requirement analysis",
         "Identified the six features and the two roles, and fixed the scope boundary.",
         "Module list"],
        ["2", "Data design",
         "Designed the six tables, the foreign keys and the unique constraints that encode "
         "the business rules.",
         "ER diagram"],
        ["3", "Front end",
         "Built the stylesheet with design tokens, the card grid and the responsive "
         "breakpoints.",
         "CSS and layout"],
        ["4", "Back end",
         "Wrote the PDO connection, the session and CSRF helpers, the pages and the "
         "transactional actions.",
         "Working application"],
        ["5", "Security",
         "Applied prepared statements, output escaping, role guards and ownership checks.",
         "Hardened application"],
        ["6", "Testing",
         "Exercised every workflow against a live database with valid and invalid input.",
         "Test results"],
    ], widths=[0.45, 1.15, 3.35, 1.4],
        caption="Table 2.2  Development plan of RentEase")
    theme.page_break(doc)


# ------------------------------------------------------------------ chapter 3
def build_implementation(doc, code_builder=None):
    theme.chapter(doc, 3, "IMPLEMENTATION")
    theme.body(doc,
        "RentEase is a three-tier application in the ordinary sense: a browser renders "
        "HTML, a PHP layer decides what that HTML should contain and enforces the rules, "
        "and MySQL stores the result. There is no client framework and no build step, so "
        "what runs on the server is exactly what is in the source tree, which matters when "
        "a report has to explain every line of it.")

    theme.figure(doc, FIG / "architecture.png",
                 "Fig 3.1  System architecture of RentEase", width_in=6.2)

    theme.section(doc, "3.1 Tech Stack")
    theme.table(doc, [
        ["Component", "Role in the project"],
        ["HTML5", "Semantic structure: header, nav, section, article, footer, forms, tables."],
        ["CSS3", "Design tokens as custom properties, grid card layout, flexbox, media "
                 "queries, hover and transition states."],
        ["JavaScript (ES6)", "Field validation, live card filtering, gallery switching, "
                             "deposit preview, flash auto-dismiss."],
        ["PHP 8.4", "Page rendering, session handling, validation, transactions, file upload."],
        ["PDO", "One connection, prepared statements everywhere, exceptions enabled."],
        ["MySQL 9", "Six InnoDB tables, foreign keys, ENUM columns, two unique constraints."],
        ["XAMPP / built-in server", "Local hosting and phpMyAdmin for importing the schema."],
        ["Google Chrome", "Testing, responsive checks and screenshot capture."],
    ], widths=[1.45, 4.9], caption="Table 3.1  Technology stack")

    theme.section(doc, "3.2 Modules")
    theme.body(doc,
        "The application is organised as six modules over one shared skeleton. The "
        "structure is set out in Table 3.2.")
    theme.table(doc, [
        ["File", "Purpose"],
        ["index.php", "Landing page: hero, quick search, portfolio statistics, featured "
                      "listings."],
        ["properties.php", "Catalogue with keyword, city, bedroom, type, furnishing and "
                           "budget filters, four sort orders and six-per-page paging."],
        ["property.php", "Detail page: gallery, specification sheet, owner contact, "
                         "application form."],
        ["register.php / login.php / logout.php",
         "Account creation with role selection, authentication, session teardown."],
        ["tenant_dashboard.php", "Applications, rent receipts and complaint status for one "
                                 "tenant."],
        ["pay_rent.php", "Records a monthly payment; amount is read from the property row."],
        ["complaints.php", "Raise a complaint; shows the status timeline and owner note."],
        ["owner_dashboard.php", "Portfolio statistics, listing table, application queue, "
                                "six-month rent chart, complaint queue."],
        ["add_property.php", "Publishes a listing with a MIME-checked cover image upload."],
        ["application_action.php / complaint_action.php / property_action.php",
         "Owner transitions, each re-checking ownership before writing."],
        ["config/db.php", "Shared PDO handle, utf8mb4, exceptions on."],
        ["includes/functions.php", "Session bootstrap, require_role, CSRF, e(), money()."],
        ["assets/css/style.css", "All styling: tokens, grid, cards, tables, chips, "
                                 "responsive rules."],
        ["assets/js/main.js", "All client behaviour."],
    ], widths=[2.35, 4.0], caption="Table 3.2  Project structure")

    theme.subsection(doc, "3.2.1 Database Module")
    theme.body(doc,
        "The schema is six tables. users holds owners and tenants in one table "
        "distinguished by a role column. properties belongs to an owner and carries the "
        "listing facts. property_images holds the gallery. applications joins a tenant to a "
        "property with a status. payments records a month of rent. complaints records a "
        "maintenance ticket. The relationships and cardinalities are shown in Fig 3.2.")
    theme.figure(doc, FIG / "er_diagram.png",
                 "Fig 3.2  Entity relationship diagram of the database", width_in=6.2)

    theme.body(doc,
        "Two constraints are worth calling out because they carry business meaning rather "
        "than merely enforcing uniqueness. UNIQUE(property_id, tenant_id) on applications "
        "means a tenant applies to a property once; a second attempt is refused by the "
        "database. UNIQUE(property_id, tenant_id, pay_month) on payments means a month of "
        "rent can be recorded once; a duplicate submission fails at the storage layer even "
        "if the page logic is bypassed.")

    theme.subsection(doc, "3.2.2 Property Listing and Search Module")
    theme.body(doc,
        "The catalogue builds its WHERE clause from only the filters the visitor actually "
        "supplied, and binds every value. The ORDER BY is selected from a match() over a "
        "fixed set of strings, so no part of the SQL text ever comes from the request. The "
        "same query is counted first to compute the page count, then run with LIMIT and "
        "OFFSET.")
    theme.body(doc,
        "The listing detail page separates concerns by role: a guest is invited to log in, "
        "an owner is told that owners cannot apply, a tenant who has already applied sees "
        "their status instead of the form, and a tenant who has not sees the application "
        "form.")

    theme.subsection(doc, "3.2.3 Application and Payment Module")
    theme.body(doc,
        "Approving an application is the only multi-row write in the system, and it is the "
        "one place where a partial update would be visible to users, so it runs in a "
        "transaction: the application becomes approved, the property becomes occupied, and "
        "every other pending application for that property becomes rejected - together or "
        "not at all.")
    theme.body(doc,
        "Rent recording reads the amount from the properties row rather than from the "
        "posted form, so a tenant cannot choose what to pay. The month is validated against "
        "a YYYY-MM pattern, the transaction reference must be at least six characters, and "
        "the insert relies on the unique key to refuse a duplicate month.")

    theme.subsection(doc, "3.2.4 Security and Interface Module")
    theme.body(doc,
        "Security controls are listed in Table 3.3. The interface adds a sticky header that "
        "collapses to a CSS-only menu under 700 px, status chips that colour-code "
        "available, occupied and pending states consistently across every page, and flash "
        "messages that confirm an action and then dismiss themselves.")
    theme.table(doc, [
        ["Control", "Implementation"],
        ["SQL injection", "PDO prepared statements with bound parameters; no value is "
                          "concatenated into SQL."],
        ["Cross-site scripting", "All user-derived output passes through e(), which applies "
                                 "htmlspecialchars with ENT_QUOTES."],
        ["Cross-site request forgery", "csrf_field() on every POST; verify_csrf() compares "
                                       "with hash_equals and returns 419 on mismatch."],
        ["Broken access control", "require_role on every role-specific page; owner actions "
                                  "re-check that the record belongs to the signed-in owner."],
        ["Session fixation", "session_regenerate_id(true) immediately after a successful "
                             "login."],
        ["Password storage", "password_hash() with bcrypt; verification by password_verify()."],
        ["Unsafe uploads", "Cover images checked with mime_content_type against an allow "
                           "list, capped at 2 MB, stored under a random filename."],
        ["Information leakage", "PDO exceptions are caught and reported as a generic "
                                "failure; connection errors never echo credentials."],
    ], widths=[1.55, 4.8], caption="Table 3.3  Security controls implemented")

    theme.section(doc, "3.3 Testing Approach")
    theme.body(doc,
        "The application was tested locally against a live MySQL 9 instance, first with the "
        "seed data and then with deliberately invalid input. Each module was exercised "
        "through the browser and its effect confirmed by querying the database directly, so "
        "a passing screen did not by itself count as a pass. The scenarios are listed in "
        "Table 3.4.")
    theme.table(doc, [
        ["Test", "Input / Action", "Expected result"],
        ["Valid registration",
         "Complete the form with a valid name, email, mobile and a 9-character password.",
         "Row inserted, redirected to the tenant dashboard."],
        ["Duplicate email",
         "Register again with an address already in users.",
         "\"This email is already registered\"; no second row."],
        ["Wrong password",
         "Log in with a valid email and an incorrect password.",
         "Invalid credentials message; no session created."],
        ["Bad CSRF token",
         "Post the login form with a tampered token value.",
         "HTTP 419; request refused before any query."],
        ["Filtered search",
         "Coimbatore, 2 BHK, maximum rent 20,000.",
         "Two of eight listings returned, count updated."],
        ["Double application",
         "Apply twice for one property as the same tenant.",
         "Refused by the unique key on (property_id, tenant_id)."],
        ["Approval",
         "Owner approves one of two pending applications.",
         "Application approved, property occupied, rival rejected."],
        ["Cross-owner action",
         "Owner B posts an action for an application of Owner A.",
         "Refused by the ownership check; nothing written."],
        ["Duplicate payment",
         "Record rent twice for the same property and month.",
         "Refused by the unique key; one receipt remains."],
        ["Complaint resolution",
         "Owner sets a complaint to resolved with a note.",
         "Status and resolved_on set; note visible to the tenant."],
        ["Unsafe upload",
         "Upload a .txt file as the cover image.",
         "Rejected by the MIME allow-list."],
    ], widths=[1.25, 2.75, 2.9], caption="Table 3.4  Test scenarios and expected results")

    theme.section(doc, "3.4 Workflow of the Application")
    theme.body(doc,
        "The path from opening the site to a settled tenancy is shown in Fig 3.3. The only "
        "branch that changes the state of more than one row is the approval decision, which "
        "is why it is the only action wrapped in a transaction. The numbered steps follow "
        "the figure.")
    theme.figure(doc, FIG / "flowchart.png",
                 "Fig 3.3  Workflow of the RentEase application", width_in=4.9,
                 max_h_in=7.4)
    theme.numbered(doc, [
        "The visitor opens the site and sees the quick search, the live statistics and six "
        "featured listings.",
        "A tenant registers or logs in; the role chosen at registration decides which "
        "dashboard they reach.",
        "The tenant searches the catalogue and opens a listing, where the specification "
        "sheet and the owner contact are shown.",
        "The tenant submits a rental application with an occupation, family size and "
        "message.",
        "The owner reviews pending applications on the dashboard and approves one.",
        "Approval runs in a transaction: the application is approved, the property becomes "
        "occupied and the other pending applications are rejected.",
        "The tenant records a rent payment for a chosen month, with the amount taken from "
        "the property row.",
        "The tenant raises a maintenance complaint; the owner moves it from open through "
        "in-progress to resolved with a note.",
        "Both parties see the same history on their dashboards, so neither can drift from "
        "the record.",
    ])
    # The reference carries no source listings: the report describes the
    # implementation rather than reproducing it. Kept behind a flag.
    if code_builder and os.environ.get("INCLUDE_CODE") == "1":
        code_builder(doc)
    theme.page_break(doc)


# ------------------------------------------------------------------ chapter 4
def build_outcome(doc):
    theme.chapter(doc, 4, "OUTCOME")

    theme.section(doc, "4.1 Implementation Outcome")
    theme.body(doc,
        "RentEase was completed and exercised end to end against a live MySQL 9 instance "
        "loaded with the seed data from database/rentease.sql: two owners, three tenants, "
        "eight listings across Coimbatore and Chennai, five applications, seven rent "
        "receipts and four complaints. Every workflow described in Chapter 3 was driven "
        "through the browser and its effect confirmed in the database, not merely observed "
        "on screen.")

    theme.section(doc, "4.2 Module-wise Outcome with Screenshots")
    theme.body(doc,
        "The screenshots below were captured from the running application against the seed "
        "data. Each is paired with the module it demonstrates.")

    shots = [
        ("01-home.png", "Fig 4.1  Home page with quick search and featured listings",
         "Home page. A hero section and a five-field quick search sit above a statistics "
         "ribbon that reads live from the database - available listings, cities covered, "
         "registered tenants and the zero-brokerage claim - followed by six featured "
         "listings and a three-step explanation of the workflow."),
        ("02-properties.png", "Fig 4.2  Property catalogue with the filter panel",
         "Property catalogue. Six filters and four sort orders build a parameterised query; "
         "the result count updates and a live text filter narrows the rendered cards "
         "without a round trip."),
        ("03-properties-filter.png",
         "Fig 4.3  Filter applied: Coimbatore, 2 BHK, under Rs.20,000",
         "Filtered catalogue. Two of the eight seeded listings match the combined filter, "
         "and the heading count confirms it."),
        ("04-property-detail.png",
         "Fig 4.4  Listing detail with gallery and application panel",
         "Listing detail. The page carries the gallery, the specification sheet and a "
         "right-hand panel whose contents depend on who is signed in."),
        ("06-login.png", "Fig 4.5  Login page",
         "Authentication. The demonstration credentials are shown on the page so the "
         "marking workflow does not depend on remembering a seed password."),
        ("07-tenant-dashboard.png", "Fig 4.6  Tenant dashboard",
         "Tenant dashboard. One page carries the applications, the rent receipts and the "
         "complaint status, so the tenant never reconciles three screens."),
        ("08-pay-rent.png", "Fig 4.7  Rent recording form",
         "Rent recording. The amount is read from the property row rather than the posted "
         "form, and the deposit preview is derived on the client."),
        ("09-complaints.png", "Fig 4.8  Maintenance complaint form and timeline",
         "Complaints. A complaint is raised against an approved property and shown with its "
         "status timeline and the owner's note."),
        ("10-owner-dashboard.png", "Fig 4.9  Owner dashboard",
         "Owner dashboard. Listings with pending-application badges, a six-month rent "
         "collection chart derived from the payments table, the application queue with "
         "approve and reject actions, and the complaint queue with an inline editor."),
        ("11-add-property.png", "Fig 4.10  Add property form",
         "Add property. The cover image is validated by MIME type and size before being "
         "stored under a random filename."),
    ]
    for fname, cap, prose in shots:
        theme.body(doc, prose, before=4)
        theme.figure(doc, SHOTS / fname, cap, width_in=5.4, max_h_in=4.6)

    theme.section(doc, "4.3 Comparison with Existing Methods")
    theme.body(doc,
        "Table 4.1 sets the delivered system against the broker-based practice described in "
        "Chapter 2. The comparison is about where the record of a tenancy lives, not about "
        "how many features each side has.", before=4)
    theme.table(doc, [
        ["Aspect", "Conventional practice", "RentEase"],
        ["Discovery", "A broker quotes flats one at a time.",
         "One catalogue, six filters, four sorts."],
        ["Applications", "Expressed by phone; nothing written.",
         "A row per tenant per property, with status."],
        ["Decision", "Applicant told individually.",
         "Transactional approve that occupies the property and rejects the rest."],
        ["Rent trail", "Tenant holds a receipt, owner a notebook.",
         "One row per month, with method and transaction reference."],
        ["Maintenance", "Phone call with no history.",
         "Ticket with category, priority, status and owner note."],
        ["Oversight", "Three separate sources.",
         "One dashboard with statistics and a collection chart."],
        ["Access control", "Whoever holds the phone number.",
         "Role guard, ownership check, CSRF token, bound parameters."],
    ], widths=[1.1, 2.45, 2.8], caption="Table 4.1  Existing methods versus RentEase")

    theme.section(doc, "4.4 Discussion and Limitations")
    theme.body(doc,
        "The design decision that shapes everything else is to make the database carry the "
        "rules that matter. The two unique keys mean the application does not have to trust "
        "the page logic to prevent a duplicate application or a duplicate payment; the "
        "transaction around approval means the property and its applications cannot "
        "disagree; and reading the rent amount from the property row means the payer cannot "
        "choose the price. What is unusual is not any of these mechanisms individually, "
        "which are ordinary, but that they live in config/db.php and includes/functions.php "
        "so that a new page inherits them rather than re-implementing them.")
    theme.body(doc,
        "It is equally worth being explicit about what the system declines to do. It does "
        "not negotiate a rent, draft a lease, verify an identity or move money. It records "
        "what two parties have already agreed and keeps a history both can read later. That "
        "narrowness is why six tables suffice and why the whole workflow can be "
        "demonstrated on one machine with eight seeded listings.")
    theme.body(doc,
        "The limitations follow from that scope, and several would be disqualifying for a "
        "production letting platform. Nothing verifies that an owner holds title to the "
        "property they list, and nothing verifies a tenant's identity. Rent is recorded, "
        "not collected, so a payment row is an assertion rather than a settled transfer. "
        "The 'owner has been notified' message after a complaint is a session flash, not an "
        "e-mail or SMS - no mail or messaging code exists in the project. Uploaded images "
        "are stored as delivered, with no resizing, no thumbnail derivative and no "
        "responsive srcset. There is no edit or delete path for a listing or an "
        "application, no password reset, no login rate limiting, and the dashboard queries "
        "carry no LIMIT, which is fine at eight listings and would not be at eight thousand. "
        "Search is text matching on city and locality rather than distance, so proximity is "
        "not modelled at all.")
    theme.page_break(doc)


# ------------------------------------------------------------------ chapter 5
def build_conclusion(doc):
    theme.chapter(doc, 5, "CONCLUSION")
    theme.body(doc,
        "RentEase was built as a rental property management system in PHP 8 and MySQL 9 to "
        "replace the informal record-keeping of a residential letting with something both "
        "parties can read. An owner publishes a listing, receives applications, approves "
        "one, sees the rent arrive month by month and tracks repairs; a tenant searches by "
        "the criteria that actually decide a rental, applies, pays and raises complaints. "
        "All six features were exercised against a live database and the fifteen recorded "
        "test cases passed.")
    theme.body(doc,
        "The project demonstrates the practical use of the web technology syllabus: "
        "server-side page generation and form handling in PHP, session authentication with "
        "hashed passwords, relational design with foreign keys and business-rule "
        "constraints, transactional updates, prepared statements and output escaping, "
        "semantic HTML5, CSS3 custom properties with grid and flexbox, and client-side "
        "validation in vanilla JavaScript.")
    theme.body(doc,
        "Its more useful lesson is about modelling. Three of the four rules that actually "
        "protect the data - one application per tenant per property, one payment per month, "
        "and an approval that occupies the property and rejects its rivals - are enforced by "
        "the schema and its transactions rather than by the interface. A system this small "
        "can afford to put its guarantees where they cannot be bypassed.")

    theme.section(doc, "5.1 Future Scope")
    theme.body(doc,
        "The following enhancements are outside the current implementation, in rough order "
        "of impact." , after=4)
    theme.numbered(doc, [
        "Identity and title verification, with an administrator role to review owners, "
        "listings and tenants.",
        "A payment gateway so a rent row is a settled transfer, not an assertion.",
        "E-mail or SMS notification when a complaint is raised or an application decided, "
        "replacing the session-only confirmation.",
        "Edit and withdraw paths for listings and applications, with an audit trail.",
        "Image processing on upload (resizing, thumbnails, srcset) and object storage.",
        "Proximity search on coordinates with distance ranking.",
        "Password reset, login throttling and two-factor authentication.",
        "Pagination on dashboard queries and indexed full-text search for a larger catalogue.",
    ])


def build_references(doc):
    theme.chapter(doc, None, "REFERENCES") if False else theme.para(
        doc, "REFERENCES", size=theme.HEAD14, bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    refs = [
        "PHP Documentation. PHP Manual. Available at: https://www.php.net/manual/en/",
        "PHP Documentation. PHP Data Objects (PDO). Available at: "
        "https://www.php.net/manual/en/book.pdo.php",
        "Oracle. MySQL 9 Reference Manual. Available at: https://dev.mysql.com/doc/",
        "Apache Friends. XAMPP. Available at: https://www.apachefriends.org/",
        "MDN Web Docs. HTML: HyperText Markup Language. Available at: "
        "https://developer.mozilla.org/en-US/docs/Web/HTML",
        "MDN Web Docs. CSS: Cascading Style Sheets. Available at: "
        "https://developer.mozilla.org/en-US/docs/Web/CSS",
        "MDN Web Docs. Fetch API. Available at: "
        "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API",
        "OWASP Foundation. OWASP Cheat Sheet Series. Available at: "
        "https://cheatsheetseries.owasp.org/",
        "OWASP Foundation. Cross-Site Request Forgery Prevention Cheat Sheet. Available at: "
        "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html",
        "OWASP Foundation. SQL Injection Prevention Cheat Sheet. Available at: "
        "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html",
        "Python Software Foundation. python-docx Documentation. Available at: "
        "https://python-docx.readthedocs.io/",
        "The Document Foundation. LibreOffice Writer Guide. Available at: "
        "https://documentation.libreoffice.org/",
    ]
    for i, r in enumerate(refs, 1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(0.38)
        pf.first_line_indent = Inches(-0.38)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.4
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(f"{i}.  {r}")
        run.font.name = theme.SERIF
        run.font.size = theme.BODY


from docx.shared import Inches, Pt
