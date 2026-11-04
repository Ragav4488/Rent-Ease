"""CHAPTER 9 - Mini Project: RentEase.

Text and listings are carried over verbatim from Report/build_report.py
(mini_project, mini_process, mini_code, mini_frontend, mini_output) and only
re-expressed through the Report2 theme helpers.
"""
from pathlib import Path

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from .. import theme

ROOT = Path(__file__).resolve().parent.parent          # .../Report2
FIG = ROOT / "figures"
SHOTS = ROOT.parent / "screenshots"

SMALL_CODE = Pt(8.5)      # the SQL examples are too wide for 11 pt


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
#  9.1  Aim, objectives, scope, stack, architecture, ER diagram, procedure
# --------------------------------------------------------------------------
def build_intro(doc):
    theme.exp_head(doc, "09", "02/11/2026",
                   "Mini Project - RentEase: Rental Property Management System")

    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design and develop a complete rental property management web application, "
                    "\"RentEase\", using HTML, CSS, JavaScript, PHP and MySQL that lets property "
                    "owners publish listings with images and lets tenants search those listings, "
                    "submit rental applications, record monthly rent payments, raise maintenance "
                    "complaints, and gives the owner a dashboard to manage the whole portfolio.")

    theme.heading_plain(doc, "OBJECTIVES:")
    theme.bullets(doc, [
        "Provide a searchable, filterable catalogue of rental properties with image galleries.",
        "Let a tenant apply for a property online and let the owner approve or reject the application.",
        "Maintain a month-by-month rent payment record against a transaction reference.",
        "Track maintenance complaints from Open through In-Progress to Resolved.",
        "Give the owner a single dashboard for listings, applications, rent collected and complaints.",
        "Enforce role-based access, CSRF protection and prepared statements throughout.",
    ])

    theme.heading_plain(doc, "SCOPE OF THE SYSTEM:")
    _keep_together(theme.table(doc, [
        ["Module", "Actors", "Functions"],
        ["Authentication", "Owner, Tenant", "Register, log in, log out, role-based redirection"],
        ["Property listing", "Owner", "Add listing, upload cover image, toggle availability"],
        ["Search & filter", "Tenant, Guest", "Keyword, city, BHK, type, furnishing, budget, sort, paging"],
        ["Rental application", "Tenant, Owner", "Apply with occupation and family size; approve or reject"],
        ["Rent payment", "Tenant, Owner", "Record monthly payment, transaction reference, receipt list"],
        ["Maintenance", "Tenant, Owner", "Raise complaint, set priority, update status, owner note"],
        ["Owner dashboard", "Owner", "Portfolio stats, rent chart, application queue, complaint queue"],
    ], widths=[1.3, 1.2, 3.8]))

    theme.heading_plain(doc, "TECHNOLOGY STACK:")
    _keep_together(theme.table(doc, [
        ["Layer", "Technology", "Used for"],
        ["Markup", "HTML5", "Semantic header, nav, section, article and footer; forms and tables"],
        ["Styling", "CSS3", "Custom properties, flexbox, grid, media queries, hover states"],
        ["Behaviour", "JavaScript (ES6)", "Field validation, live filtering, gallery, rent preview"],
        ["Server", "PHP 8.4", "Session handling, PDO queries, password hashing, file upload"],
        ["Database", "MySQL 9", "Six InnoDB tables, foreign keys, ENUM and unique constraints"],
    ], widths=[1.0, 1.5, 3.8]))

    theme.heading_plain(doc, "SYSTEM ARCHITECTURE:")
    theme.body(doc, "RentEase follows a three-tier architecture. The browser renders HTML built by "
                    "PHP and styles it with one stylesheet; the PHP layer authenticates the user, "
                    "validates the request and talks to MySQL only through PDO prepared statements; "
                    "the data layer stores six related tables in InnoDB.")
    theme.figure(doc, FIG / "architecture.png",
                 "Fig 9.1  THREE-TIER ARCHITECTURE OF RENTEASE")

    theme.heading_plain(doc, "ENTITY RELATIONSHIP DIAGRAM:")
    theme.body(doc, "A single users table holds both owners and tenants, distinguished by the role "
                    "column. One owner has many properties; one property has many images, "
                    "applications, payments and complaints; a tenant links to properties through "
                    "applications and payments.")
    theme.figure(doc, FIG / "er_diagram.png",
                 "Fig 9.2  ENTITY RELATIONSHIP DIAGRAM OF THE RENTEASE DATABASE")

    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Install PHP 8.4, MySQL 9 and a web browser; XAMPP may be used instead of a native install.",
        "Create the project folder RentEase with the subfolders config, includes, assets, "
        "database, scripts and screenshots.",
        "Create the database rentease and the six tables users, properties, property_images, "
        "applications, payments and complaints.",
        "Write config/db.php to open one shared PDO connection with exceptions enabled and "
        "utf8mb4 as the charset.",
        "Write includes/functions.php with the session bootstrap, require_login(), "
        "require_role(), the CSRF helpers and the e() output escaper.",
        "Build includes/header.php and includes/footer.php so every page shares the same "
        "navigation and footer.",
        "Design index.php with a hero banner, a quick search form and the featured listings.",
        "Design properties.php with keyword, city, BHK, type, furnishing and budget filters "
        "built as a dynamically assembled WHERE clause with bound parameters.",
        "Design property.php with an image gallery, a specification sheet and the rental "
        "application form.",
        "Implement register.php and login.php with password_hash(), password_verify() and "
        "session_regenerate_id().",
        "Implement tenant_dashboard.php, pay_rent.php and complaints.php for the tenant side.",
        "Implement owner_dashboard.php, add_property.php, application_action.php, "
        "complaint_action.php and property_action.php for the owner side.",
        "Write assets/css/style.css and assets/js/main.js for styling and client-side behaviour.",
        "Populate the tables with representative demo data from database/rentease.sql.",
        "Start the server with php -S 127.0.0.1:8088, exercise every workflow and record the "
        "screenshots for this report.",
    ])

    theme.heading_plain(doc, "DATABASE - RENTEASE.SQL:")
    theme.code(doc, """DROP DATABASE IF EXISTS rentease;
CREATE DATABASE rentease
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE rentease;

CREATE TABLE users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(80)  NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    phone         VARCHAR(15)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('owner','tenant') NOT NULL DEFAULT 'tenant',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE properties (
    property_id   INT AUTO_INCREMENT PRIMARY KEY,
    owner_id      INT NOT NULL,
    title         VARCHAR(120) NOT NULL,
    description   TEXT,
    property_type ENUM('Apartment','Independent House','Villa',
                       'PG / Hostel','Studio') NOT NULL,
    bhk           TINYINT NOT NULL,
    city          VARCHAR(60) NOT NULL,
    locality      VARCHAR(80) NOT NULL,
    address       VARCHAR(200) NOT NULL,
    rent_amount   DECIMAL(10,2) NOT NULL,
    deposit       DECIMAL(10,2) NOT NULL DEFAULT 0,
    area_sqft     INT NOT NULL,
    furnishing    ENUM('Unfurnished','Semi-Furnished','Fully-Furnished') NOT NULL,
    available_from DATE NOT NULL,
    status        ENUM('available','occupied','inactive') DEFAULT 'available',
    cover_image   VARCHAR(200),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_prop_owner FOREIGN KEY (owner_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_city (city), INDEX idx_rent (rent_amount),
    INDEX idx_bhk (bhk),   INDEX idx_status (status)
) ENGINE=InnoDB;

CREATE TABLE property_images (
    image_id    INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    image_path  VARCHAR(200) NOT NULL,
    caption     VARCHAR(120),
    CONSTRAINT fk_img_prop FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id    INT NOT NULL,
    tenant_id      INT NOT NULL,
    message        TEXT,
    occupation     VARCHAR(60),
    family_size    TINYINT DEFAULT 1,
    applied_on     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status         ENUM('pending','approved','rejected') DEFAULT 'pending',
    UNIQUE KEY uq_app (property_id, tenant_id),
    CONSTRAINT fk_app_prop   FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE,
    CONSTRAINT fk_app_tenant FOREIGN KEY (tenant_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE payments (
    payment_id  INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    tenant_id   INT NOT NULL,
    amount      DECIMAL(10,2) NOT NULL,
    pay_month   DATE NOT NULL,
    method      ENUM('UPI','Net Banking','Card','Cash') NOT NULL,
    txn_ref     VARCHAR(40) NOT NULL,
    paid_on     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_pay (property_id, tenant_id, pay_month),
    CONSTRAINT fk_pay_prop   FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE,
    CONSTRAINT fk_pay_tenant FOREIGN KEY (tenant_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id  INT NOT NULL,
    tenant_id    INT NOT NULL,
    category     ENUM('Plumbing','Electrical','Carpentry',
                      'Appliance','Cleaning','Other') NOT NULL,
    subject      VARCHAR(120) NOT NULL,
    description  TEXT NOT NULL,
    priority     ENUM('Low','Medium','High') DEFAULT 'Medium',
    status       ENUM('open','in-progress','resolved') DEFAULT 'open',
    owner_note   VARCHAR(255),
    raised_on    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_on  DATETIME NULL,
    CONSTRAINT fk_cmp_prop   FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE,
    CONSTRAINT fk_cmp_tenant FOREIGN KEY (tenant_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;""")

    theme.heading_plain(doc, "CONFIG/DB.PHP:")
    theme.body(doc, "One PDO handle is shared by every page. Exceptions are enabled so a failed "
                    "query surfaces immediately instead of failing silently.")
    theme.code(doc, """<?php
declare(strict_types=1);

const DB_HOST = '127.0.0.1';
const DB_PORT = 3306;      // 3307 in the demo environment
const DB_NAME = 'rentease';
const DB_USER = 'root';
const DB_PASS = '';        // set your local MySQL password

function db(): PDO
{
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
        DB_HOST, DB_PORT, DB_NAME);

    try {
        $pdo = new PDO($dsn, DB_USER, DB_PASS, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);
    } catch (PDOException $e) {
        http_response_code(500);
        exit('Database connection failed.');
    }

    return $pdo;
}""")

    theme.heading_plain(doc, "INCLUDES/FUNCTIONS.PHP:")
    theme.code(doc, """<?php
require_once __DIR__ . '/../config/db.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function current_user(): ?array
{
    return $_SESSION['user'] ?? null;
}

function is_owner(): bool
{
    return (current_user()['role'] ?? '') === 'owner';
}

function require_login(): void
{
    if (!current_user()) {
        header('Location: login.php?next=' .
               urlencode($_SERVER['REQUEST_URI'] ?? 'index.php'));
        exit;
    }
}

function require_role(string $role): void
{
    require_login();
    if ((current_user()['role'] ?? '') !== $role) {
        http_response_code(403);
        exit('403 - forbidden');
    }
}

function csrf_token(): string
{
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(16));
    }
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="csrf" value="' . csrf_token() . '">';
}

function verify_csrf(): void
{
    $sent = $_POST['csrf'] ?? '';
    if (!is_string($sent) || !hash_equals($_SESSION['csrf'] ?? '', $sent)) {
        http_response_code(419);
        exit('Session expired. Please reload the page.');
    }
}

function e(?string $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}

function money(float|string $amount): string
{
    return 'Rs.' . number_format((float) $amount, 0, '.', ',');
}""")


# --------------------------------------------------------------------------
#  9.2  Server-side listings, client-side files and the queries behind them
# --------------------------------------------------------------------------
def build_code(doc):
    theme.heading_plain(doc, "LOGIN.PHP - AUTHENTICATION:")
    theme.code(doc, """<?php
require_once __DIR__ . '/includes/functions.php';

if (is_logged_in()) {
    redirect(is_owner() ? 'owner_dashboard.php' : 'tenant_dashboard.php');
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $email = trim($_POST['email'] ?? '');
    $pass  = $_POST['password'] ?? '';

    $stmt = db()->prepare('SELECT * FROM users WHERE email = ? LIMIT 1');
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if ($user && password_verify($pass, $user['password_hash'])) {
        session_regenerate_id(true);          // stop session fixation
        $_SESSION['user'] = [
            'user_id'   => (int) $user['user_id'],
            'full_name' => $user['full_name'],
            'role'      => $user['role'],
        ];
        flash('Logged in as ' . $user['full_name'] . '.');
        redirect($user['role'] === 'owner'
            ? 'owner_dashboard.php'
            : 'tenant_dashboard.php');
    }

    $error = 'Invalid email or password. Please try again.';
}

$pageTitle = 'Log in';
require __DIR__ . '/includes/header.php';
?>""")

    theme.heading_plain(doc, "PROPERTIES.PHP - SEARCH AND FILTER:")
    theme.body(doc, "Filters are appended to a WHERE array only when the visitor supplied a value, "
                    "and every value is bound. The ORDER BY clause is chosen from a fixed match() "
                    "expression, so no user string ever reaches the SQL text.")
    theme.code(doc, """<?php
require_once __DIR__ . '/includes/functions.php';

const PER_PAGE = 6;

$q       = trim($_GET['q'] ?? '');
$city    = trim($_GET['city'] ?? '');
$bhk     = trim($_GET['bhk'] ?? '');
$type    = trim($_GET['type'] ?? '');
$maxRent = trim($_GET['max_rent'] ?? '');
$furnish = trim($_GET['furnishing'] ?? '');
$sort    = $_GET['sort'] ?? 'newest';
$page    = max(1, (int) ($_GET['page'] ?? 1));

$where  = ['p.status <> "inactive"'];
$params = [];

if ($q !== '') {
    $where[] = '(p.title LIKE ? OR p.locality LIKE ? OR p.city LIKE ? '
             . 'OR p.address LIKE ?)';
    $like = '%' . $q . '%';
    array_push($params, $like, $like, $like, $like);
}
if ($city !== '') {
    $where[]  = 'p.city = ?';
    $params[] = $city;
}
if ($bhk !== '') {
    $where[]  = 'p.bhk = ?';
    $params[] = (int) $bhk;
}
if ($type !== '') {
    $where[]  = 'p.property_type = ?';
    $params[] = $type;
}
if ($maxRent !== '') {
    $where[]  = 'p.rent_amount <= ?';
    $params[] = (float) $maxRent;
}
if ($furnish !== '') {
    $where[]  = 'p.furnishing = ?';
    $params[] = $furnish;
}

$orderBy = match ($sort) {
    'rent_asc'  => 'p.rent_amount ASC',
    'rent_desc' => 'p.rent_amount DESC',
    'area_desc' => 'p.area_sqft DESC',
    default     => 'p.created_at DESC',
};

$sqlWhere = 'WHERE ' . implode(' AND ', $where);

$cnt = db()->prepare("SELECT COUNT(*) FROM properties p $sqlWhere");
$cnt->execute($params);
$total  = (int) $cnt->fetchColumn();
$pages  = max(1, (int) ceil($total / PER_PAGE));
$page   = min($page, $pages);
$offset = ($page - 1) * PER_PAGE;

$stmt = db()->prepare(
    "SELECT p.*, u.full_name AS owner_name
       FROM properties p
       JOIN users u ON u.user_id = p.owner_id
      $sqlWhere
      ORDER BY $orderBy
      LIMIT " . PER_PAGE . " OFFSET $offset"
);
$stmt->execute($params);
$rows = $stmt->fetchAll();
?>""")

    theme.heading_plain(doc, "PROPERTY.PHP - RENTAL APPLICATION:")
    theme.code(doc, """<?php
$id = (int) ($_GET['id'] ?? 0);

$stmt = db()->prepare(
    'SELECT p.*, u.full_name AS owner_name
       FROM properties p
       JOIN users u ON u.user_id = p.owner_id
      WHERE p.property_id = ?'
);
$stmt->execute([$id]);
$p = $stmt->fetch();

if (!$p) {
    http_response_code(404);
    exit('Listing not found');
}

/* show the current tenant's status, if they already applied */
$myApplication = null;
if (is_tenant()) {
    $s = db()->prepare('SELECT status, applied_on FROM applications
                         WHERE property_id = ? AND tenant_id = ?');
    $s->execute([$id, current_user()['user_id']]);
    $myApplication = $s->fetch() ?: null;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_login();

    if (!is_tenant()) {
        $error = 'Only tenant accounts can apply for a property.';
    } else {
        verify_csrf();

        $message    = trim($_POST['message'] ?? '');
        $occupation = trim($_POST['occupation'] ?? '');
        $family     = max(1, (int) ($_POST['family_size'] ?? 1));

        if ($myApplication) {
            $error = 'You have already applied for this property.';
        } elseif (mb_strlen($message) < 15) {
            $error = 'Please write at least 15 characters about yourself.';
        } else {
            $ins = db()->prepare(
                'INSERT INTO applications
                   (property_id, tenant_id, message, occupation, family_size)
                 VALUES (?, ?, ?, ?, ?)'
            );
            $ins->execute([$id, current_user()['user_id'],
                           $message, $occupation, $family]);

            flash('Application submitted. The owner will review it shortly.');
            redirect('property.php?id=' . $id);
        }
    }
}
?>""")

    theme.heading_plain(doc, "PAY_RENT.PHP - RENT PAYMENT RECORD:")
    theme.body(doc, "The amount is taken from the properties row rather than from the form, so a "
                    "tenant cannot alter it, and the unique key on (property_id, tenant_id, "
                    "pay_month) makes a second payment for the same month fail at the database.")
    theme.code(doc, """<?php
require_once __DIR__ . '/includes/functions.php';
require_role('tenant');

$uid = (int) current_user()['user_id'];

/* only approved rentals can receive a payment */
$rentals = db()->prepare(
    'SELECT p.property_id, p.title, p.rent_amount
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.tenant_id = ? AND a.status = "approved"'
);
$rentals->execute([$uid]);
$rentals = $rentals->fetchAll();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $propId = (int) ($_POST['property_id'] ?? 0);
    $month  = ($_POST['pay_month'] ?? '') . '-01';
    $method = $_POST['method'] ?? 'UPI';
    $txn    = trim($_POST['txn_ref'] ?? '');

    if (!in_array($propId, array_map('intval',
            array_column($rentals, 'property_id')), true)) {
        $errors[] = 'Select a property you are approved for.';
    }
    if (!preg_match('/^\\d{4}-\\d{2}$/', $_POST['pay_month'] ?? '')) {
        $errors[] = 'Choose the month you are paying for.';
    }
    if (strlen($txn) < 6) {
        $errors[] = 'Enter a valid transaction reference.';
    }

    if (empty($errors)) {
        $amount = 0.0;
        foreach ($rentals as $r) {
            if ((int) $r['property_id'] === $propId) {
                $amount = (float) $r['rent_amount'];   // authoritative amount
            }
        }

        try {
            $ins = db()->prepare(
                'INSERT INTO payments
                   (property_id, tenant_id, amount, pay_month, method, txn_ref)
                 VALUES (?, ?, ?, ?, ?, ?)'
            );
            $ins->execute([$propId, $uid, $amount, $month, $method, $txn]);

            flash('Rent of ' . money($amount) .
                  ' recorded for ' . month_label($month) . '.');
            redirect('tenant_dashboard.php');

        } catch (PDOException $ex) {
            $errors[] = 'Rent for that month has already been recorded.';
        }
    }
}
?>""")

    theme.heading_plain(doc, "COMPLAINTS.PHP - MAINTENANCE TRACKING:")
    theme.code(doc, """<?php
require_once __DIR__ . '/includes/functions.php';
require_role('tenant');

$uid = (int) current_user()['user_id'];

$rentals = db()->prepare(
    'SELECT p.property_id, p.title
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.tenant_id = ? AND a.status = "approved"'
);
$rentals->execute([$uid]);
$rentals = $rentals->fetchAll();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $propId  = (int) ($_POST['property_id'] ?? 0);
    $cat     = $_POST['category'] ?? 'Other';
    $subject = trim($_POST['subject'] ?? '');
    $desc    = trim($_POST['description'] ?? '');
    $prio    = $_POST['priority'] ?? 'Medium';

    $allowed = array_map(fn($r) => (int) $r['property_id'], $rentals);

    if (!in_array($propId, $allowed, true)) {
        $errors[] = 'Choose one of your approved properties.';
    }
    if (mb_strlen($subject) < 6) {
        $errors[] = 'Subject must be at least 6 characters.';
    }
    if (mb_strlen($desc) < 15) {
        $errors[] = 'Describe the problem in at least 15 characters.';
    }

    if (empty($errors)) {
        $ins = db()->prepare(
            'INSERT INTO complaints
               (property_id, tenant_id, category, subject, description, priority)
             VALUES (?, ?, ?, ?, ?, ?)'
        );
        $ins->execute([$propId, $uid, $cat, $subject, $desc, $prio]);

        flash('Complaint raised. The owner has been notified.');
        redirect('complaints.php');
    }
}
?>""")

    theme.heading_plain(doc, "APPLICATION_ACTION.PHP - OWNER APPROVAL:")
    theme.body(doc, "Approving an application is transactional: the application becomes approved, "
                    "the property becomes occupied and every other pending application for that "
                    "property is rejected, so a property can never end up with two approved tenants.")
    theme.code(doc, """<?php
require_once __DIR__ . '/includes/functions.php';
require_role('owner');
verify_csrf();

$appId    = (int) ($_POST['application_id'] ?? 0);
$decision = $_POST['decision'] ?? '';

if (!in_array($decision, ['approved', 'rejected'], true)) {
    flash('Invalid decision.', 'error');
    redirect('owner_dashboard.php');
}

/* the application must belong to one of THIS owner's properties */
$check = db()->prepare(
    'SELECT a.application_id, a.property_id, a.status, p.title
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.application_id = ? AND p.owner_id = ?'
);
$check->execute([$appId, current_user()['user_id']]);
$app = $check->fetch();

if (!$app || $app['status'] !== 'pending') {
    flash('Application not found or already decided.', 'error');
    redirect('owner_dashboard.php');
}

$pdo = db();
$pdo->beginTransaction();

try {
    $pdo->prepare('UPDATE applications SET status = ? WHERE application_id = ?')
        ->execute([$decision, $appId]);

    if ($decision === 'approved') {
        $pdo->prepare('UPDATE properties SET status = "occupied" WHERE property_id = ?')
            ->execute([$app['property_id']]);

        $pdo->prepare(
            'UPDATE applications SET status = "rejected"
              WHERE property_id = ? AND status = "pending"
                AND application_id <> ?'
        )->execute([$app['property_id'], $appId]);
    }

    $pdo->commit();
} catch (PDOException $ex) {
    $pdo->rollBack();
    flash('Could not update the application.', 'error');
    redirect('owner_dashboard.php');
}

flash('Application ' . $decision . '.');
redirect('owner_dashboard.php');""")

    theme.heading_plain(doc, "ASSETS/CSS/STYLE.CSS - KEY RULES:")
    theme.code(doc, """   :root{
     --ink:#12202e;
     --ink-soft:#4b6076;
     --line:#dfe6ee;
     --bg:#f5f7fb;
     --brand:#0f766e;
     --brand-dark:#0b5c56;
     --brand-tint:#e6f4f2;
     --shadow:0 1px 2px rgba(18,32,46,.06), 0 8px 24px rgba(18,32,46,.07);
     --radius:14px;
   }

   body{
     font-family:"Segoe UI", Roboto, Arial, sans-serif;
     font-size:15px;
     line-height:1.55;
     color:var(--ink);
     background:var(--bg);
   }

   /* property cards reflow from 3 columns down to 1 */
   .cards{
     display:grid;
     grid-template-columns:repeat(auto-fill, minmax(280px,1fr));
     gap:1.2rem;
   }

   .prop-card{
     background:#fff;
     border:1px solid var(--line);
     border-radius:var(--radius);
     overflow:hidden;
     box-shadow:var(--shadow);
     transition:transform .16s ease, box-shadow .16s ease;
   }

   .prop-card:hover{
     transform:translateY(-3px);
     box-shadow:0 12px 28px rgba(18,32,46,.13);
   }

   .prop-thumb{position:relative;aspect-ratio:16/10;overflow:hidden}
   .prop-thumb img{width:100%;height:100%;object-fit:cover}

   .price-tag{
     position:absolute; left:.7rem; bottom:.7rem;
     background:rgba(18,32,46,.88); color:#fff;
     padding:.3rem .6rem; border-radius:8px;
     font-size:.86rem; font-weight:700;
   }

   /* status chips */
   .chip-green{background:#dcfce7;color:#15803d}
   .chip-blue {background:#e0f2fe;color:#0369a1}
   .chip-amber{background:#fef3c7;color:#b45309}
   .chip-red  {background:#fee2e2;color:#b91c1c}

   /* sticky header with a CSS-only mobile menu */
   .site-header{position:sticky;top:0;z-index:30;background:#fff;
                border-bottom:1px solid var(--line)}
   .header-inner{display:flex;align-items:center;
                 justify-content:space-between;min-height:66px}

   @media (max-width:700px){
     .nav-burger{display:grid;gap:4px;cursor:pointer}
     .site-nav{display:none;flex-direction:column;
               position:absolute;top:66px;left:0;right:0;
               background:#fff;padding:1rem 4vw}
     .nav-toggle:checked ~ .site-nav{display:flex}
   }""")

    theme.heading_plain(doc, "ASSETS/JS/MAIN.JS - CLIENT-SIDE VALIDATION:")
    theme.code(doc, """const rules = {
    full_name: v => v.trim().length >= 3 || 'Enter your full name',
    email:     v => /^[^\\s@]+@[^\\s@]+\\.[a-z]{2,}$/i.test(v.trim())
                  || 'Enter a valid email address',
    phone:     v => /^[6-9]\\d{9}$/.test(v.trim()) || 'Enter a 10-digit mobile',
    password:  v => v.length >= 8 || 'Minimum 8 characters',
    confirm:   v => v === document.getElementById('password').value
                  || 'Passwords do not match',
    rent_amount: v => Number(v) > 0 || 'Rent must be greater than zero',
    area_sqft:   v => Number(v) > 0 || 'Area must be greater than zero',
    subject:     v => v.trim().length >= 6 || 'Subject too short',
    description: v => v.trim().length >= 15 || 'Describe the problem'
};

document.querySelectorAll('form[data-validate]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
        let firstBad = null;

        form.querySelectorAll('input, select, textarea').forEach(function (f) {
            const rule = rules[f.name];
            if (!rule) return;

            const result = rule(f.value);
            const ok     = result === true;
            const box    = form.querySelector('[data-error-for="' + f.name + '"]');

            f.classList.toggle('invalid', !ok);
            if (box) {
                box.textContent   = ok ? '' : result;
                box.style.display = ok ? 'none' : 'block';
            }
            if (!ok && !firstBad) firstBad = f;
        });

        if (firstBad) {
            event.preventDefault();
            firstBad.focus();
        }
    });
});

/* live filter over the rendered property cards */
const live = document.getElementById('liveFilter');
if (live) {
    live.addEventListener('input', function () {
        const q = this.value.toLowerCase();
        let shown = 0;

        document.querySelectorAll('.prop-card').forEach(function (card) {
            const hit = (card.dataset.search || '').toLowerCase().includes(q);
            card.style.display = hit ? '' : 'none';
            if (hit) shown++;
        });

        document.getElementById('filterCount').textContent = shown;
    });
}""")

    theme.heading_plain(doc, "SAMPLE QUERIES USED BY THE APPLICATION:")
    _keep_together(theme.table(doc, [
        ["Purpose", "SQL"],
        ["Login", "SELECT * FROM users WHERE email = ? LIMIT 1"],
        ["Filtered listing", "SELECT p.*, u.full_name FROM properties p JOIN users u ON u.user_id = p.owner_id WHERE p.status <> 'inactive' AND p.city = ? AND p.bhk = ? ORDER BY p.created_at DESC LIMIT 6 OFFSET 0"],
        ["Tenant applications", "SELECT a.*, p.title FROM applications a JOIN properties p ON p.property_id = a.property_id WHERE a.tenant_id = ? ORDER BY a.applied_on DESC"],
        ["Owner rent chart", "SELECT DATE_FORMAT(pay_month,'%b %Y') AS label, SUM(amount) AS total FROM payments pay JOIN properties p ON p.property_id = pay.property_id WHERE p.owner_id = ? AND pay_month >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) GROUP BY label ORDER BY pay_month"],
        ["Complaint queue", "SELECT c.*, p.title, u.full_name FROM complaints c JOIN properties p ON p.property_id = c.property_id JOIN users u ON u.user_id = c.tenant_id WHERE p.owner_id = ? ORDER BY FIELD(c.status,'open','in-progress','resolved')"],
    ], widths=[1.3, 5.0], size=SMALL_CODE))


# --------------------------------------------------------------------------
#  9.3  Screenshots of the running application, Fig 9.3 .. Fig 9.13
# --------------------------------------------------------------------------
def build_output(doc):
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "The application was started with php -S 127.0.0.1:8088 against a live MySQL 9 "
                    "instance holding the seed data from database/rentease.sql. The screens below "
                    "were captured from the running application.")

    for fname, cap in [
        ("01-home.png", "Fig 9.3  Home page - hero search, portfolio statistics and featured listings"),
        ("02-properties.png", "Fig 9.4  Property listing page with the full filter panel"),
        ("03-properties-filter.png", "Fig 9.5  Filter applied (Coimbatore, 2 BHK, under Rs.20,000) - 2 of 8 match"),
        ("04-property-detail.png", "Fig 9.6  Property detail - gallery, specification sheet and application panel"),
        ("05-register.png", "Fig 9.7  Registration page with the owner / tenant role selector"),
        ("06-login.png", "Fig 9.8  Login page with the demo credentials panel"),
        ("07-tenant-dashboard.png", "Fig 9.9  Tenant dashboard - applications, rent receipts and complaint status"),
        ("08-pay-rent.png", "Fig 9.10  Rent payment form; the amount comes from the property record"),
        ("09-complaints.png", "Fig 9.11  Complaint form with the status timeline and the owner's note"),
        ("10-owner-dashboard.png", "Fig 9.12  Owner dashboard - portfolio statistics, listings, rent chart, application and complaint queues"),
        ("11-add-property.png", "Fig 9.13  Add property form with cover-image upload"),
    ]:
        theme.figure(doc, SHOTS / fname, cap, width_in=6.35, max_h_in=9.0)
