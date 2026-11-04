"""CHAPTER 9 - comparison, discussion and result.

build_comparison and build_limits are written for this theme; every claim is
grounded in the PHP sources in the project root (properties.php,
application_action.php, pay_rent.php, complaint_action.php, owner_dashboard.php,
add_property.php, includes/functions.php).  build_result carries the testing
table, the result paragraph and the rubric block over from
Report/build_report.py::mini_result, verbatim.
"""
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from .. import theme


def _keep_together(tbl):
    """Typography for a table that may run over a page.

    Rows are not split across pages, the head repeats on the continuation, and
    the caption paragraph directly above the table is tied to it so the two
    never end up on different pages.

    Every element is added only if absent: theme.table() already marks rows
    with w:cantSplit, and a second w:cantSplit in one w:trPr is invalid OOXML.
    """
    for row in tbl.rows:
        tr_pr = row._tr.get_or_add_trPr()
        if tr_pr.find(qn("w:cantSplit")) is None:
            tr_pr.insert(0, OxmlElement("w:cantSplit"))

    head_pr = tbl.rows[0]._tr.get_or_add_trPr()
    if head_pr.find(qn("w:tblHeader")) is None:
        head_pr.append(OxmlElement("w:tblHeader"))

    prev = tbl._tbl.getprevious()
    if prev is not None and prev.tag == qn("w:p"):
        p_pr = prev.get_or_add_pPr()
        if p_pr.find(qn("w:keepNext")) is None:
            p_pr.append(OxmlElement("w:keepNext"))
    return tbl


# --------------------------------------------------------------------------
#  9.4  How RentEase differs from broker-based rental search
# --------------------------------------------------------------------------
def build_comparison(doc):
    theme.body(doc, "The problem RentEase addresses is not new. Rental search in an Indian "
                    "city is normally held together by brokers, telephone calls and "
                    "photographs forwarded over chat, and none of those three keeps a "
                    "record that the other two can read. The application does not try to "
                    "replace the conversation between an owner and a tenant; it moves the "
                    "steps that produce a record - the listing, the application, the owner's "
                    "decision, the monthly receipt and the maintenance complaint - into one "
                    "MySQL database that both parties read from. Table 9.1 sets the two "
                    "workflows side by side.")

    _keep_together(theme.table(doc, [
        ["Aspect", "Conventional practice", "RentEase"],
        ["Listing discovery",
         "Units reach a tenant one broker at a time, and the same flat may be quoted "
         "differently by each.",
         "Every listing sits in the properties table and is browsable by anyone through "
         "index.php and properties.php without an account."],
        ["Search criteria",
         "Whatever the broker remembers, usually a city and a budget.",
         "Keyword, city, BHK, property type, furnishing and maximum rent are combined in "
         "one query, with four sort orders and six listings to a page."],
        ["Applications",
         "Discussed on the phone; no common record of who applied for what, or when.",
         "One applications row per tenant per property carrying occupation, family size "
         "and a message; a unique key refuses a second application."],
        ["Owner decision",
         "Each applicant is telephoned individually and told the outcome.",
         "The owner approves or rejects from the dashboard; approval runs in one "
         "transaction that marks the property occupied and rejects the other pending "
         "applications."],
        ["Rent records",
         "A handwritten receipt for the tenant and a separate notebook for the owner.",
         "One payments row per month with amount, method and transaction reference; the "
         "amount is taken from the property row and a unique key refuses a duplicate "
         "month."],
        ["Maintenance complaints",
         "A telephone call that leaves no history once the call ends.",
         "A complaint row with category and priority moving from open to in-progress to "
         "resolved, with an owner note and a resolved timestamp."],
        ["Owner oversight",
         "Rent due, pending requests and repairs are tracked in three separate places.",
         "owner_dashboard.php shows listings, rent collected, a six-month collection "
         "chart, the application queue and the complaint queue on one page."],
        ["Image galleries",
         "Photographs sent over chat and lost as the thread scrolls away.",
         "A cover image stored on the server plus a property_images gallery that "
         "JavaScript swaps into the main frame."],
        ["Security",
         "Contact details passed by word of mouth, with no record of who saw what.",
         "Hashed passwords, a role guard on every private page, a CSRF token on every "
         "POST and bound parameters in every query."],
        ["Availability status",
         "Remembered by the broker; flats that are already let stay advertised.",
         "Each property carries available, occupied or inactive, toggled by the owner and "
         "filtered out of the public catalogue when it is inactive."],
    ], widths=[1.3, 2.4, 2.6],
        caption="Table 9.1  RENTEASE VERSUS CONVENTIONAL BROKER-BASED RENTAL SEARCH"))

    theme.body(doc, "Read down the two right-hand columns, the difference is less about "
                    "features than about where the truth of a tenancy lives. In the "
                    "conventional workflow the tenant holds a receipt, the owner holds a "
                    "notebook and the broker holds the contact list, so no one can answer a "
                    "dispute from documents alone. In RentEase a single payments table is the "
                    "record: the tenant's dashboard lists its rows, the owner's dashboard "
                    "sums the same rows, and neither figure can drift from the other. The "
                    "same holds for applications and complaints, which is why the schema "
                    "needs no reconciliation step.")


# --------------------------------------------------------------------------
#  9.5  What the implementation demonstrates, and where it stops
# --------------------------------------------------------------------------
def build_limits(doc):
    _keep_together(theme.table(doc, [
        ["Outcome", "Value", "Meaning"],
        ["Property search",
         "Six filters, four sorts",
         "Keyword, city, BHK, type, furnishing and budget are combined in one bound "
         "query, six listings to a page."],
        ["Application flow",
         "Three states",
         "pending, approved or rejected, with a unique key that stops a tenant applying "
         "twice for one property."],
        ["Owner decision",
         "One transaction",
         "Approval sets the property to occupied and rejects the remaining pending "
         "applications, or none of it happens."],
        ["Rent records",
         "One row per month",
         "Amount, method and transaction reference per month; a duplicate month is "
         "refused by the database."],
        ["Maintenance",
         "Three-stage queue",
         "open, in-progress and resolved, each with a priority, an owner note and a "
         "resolved timestamp."],
        ["Security",
         "Applied at the includes",
         "password_hash, session_regenerate_id, role guards, CSRF tokens, prepared "
         "statements and escaped output."],
        ["Interface",
         "Responsive",
         "CSS Grid and Flexbox with a sticky header, collapsing to a single column below "
         "700 px."],
    ], widths=[1.3, 1.35, 3.6], caption="Table 9.2  KEY OUTCOMES OF RENTEASE"))

    theme.body(doc, "Read together, the outcomes in Table 9.2 describe an application whose "
                    "correctness rests on the database rather than on every page remembering "
                    "to check. The unique keys on applications and on (property_id, "
                    "tenant_id, pay_month) in payments make a second application and a second "
                    "payment impossible to store, not merely unlikely; approving an "
                    "application runs inside a transaction, so the property, the approved "
                    "tenant and the rejected applicants change together or not at all; and the "
                    "amount credited for rent is read from the properties row instead of the "
                    "posted form, so a tenant cannot choose what to pay.")

    theme.body(doc, "The listing side shows the same preference for the database. A filtered "
                    "search appends one condition per supplied value and binds every value, "
                    "and the ORDER BY clause is chosen from a fixed match() expression, so the "
                    "SQL text is assembled from a closed set of fragments. Every private page "
                    "opens with require_role(), every POST carries a token compared with "
                    "hash_equals(), and every value printed back into HTML passes through e(). "
                    "None of these measures is unusual in itself; what matters is that they "
                    "live in includes/functions.php and config/db.php, so a new page inherits "
                    "them instead of re-implementing them.")

    theme.body(doc, "It is equally worth being clear about what the application declines to "
                    "do. It does not negotiate a rent, draft a lease or verify an identity; it "
                    "records what the owner and the tenant have already agreed and keeps a "
                    "history that either side can read later. That narrowness is why six "
                    "tables - users, properties, property_images, applications, payments and "
                    "complaints - are enough, and why the whole workflow could be demonstrated "
                    "on one machine with a seeded catalogue of eight listings.")

    theme.body(doc, "The limitations follow from the same scope. Nothing in RentEase verifies "
                    "the people who use it: registration asks only for a name, an e-mail, a "
                    "phone number and a password, so no owner is proved to hold title to the "
                    "property they list and no tenant is proved able to pay, and a guest can "
                    "browse the catalogue with no verification at all. Payments are recorded "
                    "rather than processed - there is no payment gateway, the transaction "
                    "reference is typed by the tenant and is never checked against a bank - so "
                    "the application holds a claim of payment, not evidence of one. Images are "
                    "written into a local assets/properties directory with no resizing and no "
                    "srcset, so a listing card hands the browser a full-size upload; the "
                    "2 MB cap on the cover exists for that reason and not as a security boundary.")

    theme.body(doc, "The remaining limits are operational. Every filter compares an exact "
                    "value or a LIKE pattern, so a locality spelt differently returns nothing "
                    "and there is no map or distance search. The dashboards select their rows "
                    "without a LIMIT, which is harmless for eight listings and will not stay "
                    "harmless for a few thousand. There is no password reset, no lockout or "
                    "rate limit on repeated logins, and no delete or edit path for a property "
                    "or an application. The flash message that tells a tenant the owner has "
                    "been notified only writes to the session - no e-mail or SMS is sent. "
                    "Finally, the application was exercised by hand on a single XAMPP machine "
                    "with two owners, three tenants and eight listings: the fifteen cases in "
                    "Table 9.3 are functional checks and not an automated suite, and no part "
                    "of the design has been measured under concurrent load.")

    theme.heading_plain(doc, "FUTURE SCOPE:")
    theme.bullets(doc, [
        "Identity verification for owners and tenants before a listing or an application "
        "becomes visible to the other side.",
        "Integration with a payment gateway so that a transaction reference is issued by the "
        "provider instead of being typed by the tenant.",
        "Password reset by e-mail, and login throttling after repeated failures.",
        "E-mail and SMS delivery for the events that are currently only flashed on screen.",
        "Server-side image resizing and a thumbnail variant, or an image CDN, so a listing "
        "page stops shipping full-size uploads.",
        "A LIMIT with server-side pagination on the dashboard result sets before a portfolio "
        "grows past a handful of listings.",
        "Alias matching for localities, and a map or distance-based search alongside the "
        "existing filters.",
        "Edit and withdraw paths for listings and applications, with the audit trail that "
        "makes them safe to offer.",
        "An automated suite that replays the fifteen cases in Table 9.3 on every change.",
    ])


# --------------------------------------------------------------------------
#  9.6  Testing, result and rubrics
# --------------------------------------------------------------------------
def build_result(doc):
    theme.heading_plain(doc, "TESTING:")
    theme.body(doc, "Every workflow was exercised against the live database. The table records "
                    "the test cases, the expected result and the observed result.")
    _keep_together(theme.table(doc, [
        ["#", "Test case", "Expected result", "Status"],
        ["1", "Register a new tenant", "Row inserted, redirected to tenant dashboard", "Pass"],
        ["2", "Register with an existing email", "\"This email is already registered\"", "Pass"],
        ["3", "Log in with a wrong password", "Invalid email or password message", "Pass"],
        ["4", "Open a POST form with a bad CSRF token", "HTTP 419, request refused", "Pass"],
        ["5", "Filter Coimbatore + 2 BHK + max 20,000", "2 of 8 listings returned", "Pass"],
        ["6", "Tenant applies for a property", "Application stored as pending", "Pass"],
        ["7", "Tenant applies twice for the same property", "Refused, unique key respected", "Pass"],
        ["8", "Owner approves an application", "Application approved, property occupied", "Pass"],
        ["9", "Owner B acts on owner A's application", "Refused by the ownership check", "Pass"],
        ["10", "Record rent for a new month", "Payment row with the property's rent", "Pass"],
        ["11", "Record rent twice for one month", "Refused, unique key respected", "Pass"],
        ["12", "Tenant raises a complaint", "Complaint stored as open", "Pass"],
        ["13", "Owner marks a complaint resolved", "Status resolved, resolved_on set", "Pass"],
        ["14", "Owner adds a property with an image", "Row plus one gallery image created", "Pass"],
        ["15", "Upload a non-image file as cover", "Rejected by the MIME check", "Pass"],
    ], widths=[0.4, 2.45, 2.65, 0.85],
        caption="Table 9.3  TEST CASES AND OBSERVED RESULTS"))

    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the RentEase rental property management system was designed and developed "
                    "using HTML, CSS, JavaScript, PHP and MySQL. The application supports property "
                    "listings with image galleries, multi-facet search and filtering, online rental "
                    "applications with owner approval, month-by-month rent payment records, "
                    "maintenance complaint tracking and a consolidated owner dashboard. All six "
                    "features were verified against a live MySQL database and the fifteen test "
                    "cases above passed.")
    _keep_together(theme.rubric_table(doc))

    # end of Chapter 9 - the boundary with the next chapter
    theme.page_break(doc)
