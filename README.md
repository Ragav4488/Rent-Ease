# RentEase — Rental Property Management System

A complete rental-property platform for owners and tenants, built with **HTML, CSS,
JavaScript, PHP and MySQL**. Owners list properties and manage applications, rent and
maintenance; tenants search, apply, pay rent and raise complaints.

Built as the **Mini Project (Ex. No. 09)** for **U21CS504 — Web Technologies Laboratory**,
Department of CSE, KPR Institute of Engineering and Technology.

---

## Feature checklist

| Requirement | Where it lives |
|---|---|
| Property listing with images | `properties.php`, `property.php`, `property_images` table |
| Search and filter properties | `properties.php` (keyword, city, BHK, type, furnishing, budget, sort, pagination) |
| Rental applications | `property.php` (apply form), `application_action.php` (owner decision) |
| Rent payment records | `pay_rent.php`, `tenant_dashboard.php`, `payments` table |
| Maintenance complaint tracking | `complaints.php`, `complaint_action.php`, `complaints` table |
| Owner dashboard | `owner_dashboard.php` (stats, listings, applications, rent chart, complaint queue) |

Extras: role-based authentication, CSRF tokens on every POST, prepared statements
everywhere, image upload with MIME sniffing, duplicate-payment protection, and
ownership checks so one owner can never act on another owner's records.

---

## Tech stack

| Layer | Technology |
|---|---|
| Markup | HTML5 (semantic `header`/`nav`/`section`/`footer`) |
| Styling | CSS3 — custom properties, flexbox, grid, media queries, `:has()` |
| Behaviour | Vanilla JavaScript — validation, live filtering, gallery, flash auto-dismiss |
| Server | PHP 8.4 (PDO, `password_hash`, sessions) |
| Database | MySQL 9 (`InnoDB`, foreign keys, `ENUM`, unique constraints) |

No frameworks, no build step, no Composer dependencies.

---

## Directory layout

```
RentEase/
├── index.php                 landing page + featured listings
├── properties.php            search / filter / sort / paginate
├── property.php              gallery + specs + apply form
├── register.php              sign up as owner or tenant
├── login.php                 authentication
├── logout.php                session teardown
├── tenant_dashboard.php      applications, payments, complaints
├── owner_dashboard.php       portfolio, applications, rent chart, complaints
├── pay_rent.php              record a monthly rent payment
├── complaints.php            raise a complaint + status timeline
├── add_property.php          new listing with cover image upload
├── application_action.php    owner approve / reject
├── complaint_action.php      owner status update
├── property_action.php       owner availability toggle
├── config/db.php             PDO connection
├── includes/functions.php    session, guards, CSRF, helpers
├── includes/header.php       shared navigation
├── includes/footer.php       shared footer
├── assets/css/style.css      all styling
├── assets/js/main.js         all client-side behaviour
├── assets/properties/        listing images
├── database/rentease.sql          MySQL schema + seed
└── database/seed_sqlite.sql       portable seed used by the fallback
```

---

## Running it

### 1. Start MySQL and import the database

```bash
mysql -u root -p < database/rentease.sql
```

This drops and recreates the `rentease` database with all six tables and demo data.

### 2. Point the app at your server

Edit `config/db.php`:

```php
const DB_HOST = '127.0.0.1';
const DB_PORT = 3306;      // XAMPP/WAMP default; this build's demo used 3307
const DB_NAME = 'rentease';
const DB_USER = 'root';
const DB_PASS = '';        // your MySQL password
```

### 3. Serve it

With XAMPP/WAMP, copy `RentEase/` into `htdocs/` and open
<http://localhost/RentEase/>.

Without XAMPP, PHP's built-in server is enough:

```bash
cd RentEase
php -S 127.0.0.1:8088
```

Then open <http://127.0.0.1:8088/>.

### Demo accounts

| Role | Email | Password |
|---|---|---|
| Owner | `ragav.owner@rentease.in` | `rent@1234` |
| Owner | `meera.owner@rentease.in` | `rent@1234` |
| Tenant | `arjun.tenant@rentease.in` | `rent@1234` |
| Tenant | `divya.tenant@rentease.in` | `rent@1234` |
| Tenant | `karthik.tenant@rentease.in` | `rent@1234` |

---

## Database schema

```
users ──┬──< properties ──┬──< property_images
        │                 ├──< applications >── users (tenant)
        │                 ├──< payments     >── users (tenant)
        │                 └──< complaints   >── users (tenant)
        └──< applications / payments / complaints (as the tenant)
```

| Table | Purpose | Notable constraints |
|---|---|---|
| `users` | owners and tenants in one login table | `email` UNIQUE, `role` ENUM |
| `properties` | listings | FK `owner_id`, indexes on city/rent/bhk/status |
| `property_images` | gallery rows | FK cascade delete |
| `applications` | rental applications | `UNIQUE(property_id, tenant_id)` stops duplicates |
| `payments` | rent receipts | `UNIQUE(property_id, tenant_id, pay_month)` stops double payment |
| `complaints` | maintenance tickets | FK cascade, `resolved_on` set on resolution |

---

## Security notes

- Every query that touches user input is a **prepared statement**; there is no string
  concatenation of values into SQL.
- All POST forms carry a **CSRF token** compared with `hash_equals`; a bad token returns
  HTTP 419.
- Passwords are stored with `password_hash()` (bcrypt cost 12) and checked with
  `password_verify()`.
- `session_regenerate_id(true)` runs on login to prevent session fixation.
- Owner actions re-verify that the target record belongs to the signed-in owner before
  any write (`application_action.php`, `complaint_action.php`, `property_action.php`).
- Uploads are validated by `mime_content_type()` against an allow-list and capped at 2 MB,
  then stored under a random filename.
- All output passes through `e()` (`htmlspecialchars`, `ENT_QUOTES`, UTF-8).

---

## Hosting

Free hosts have no MySQL service, so the app does this automatically:

1. Tries MySQL first.
2. Falls back to SQLite, creating and seeding `database/rentease.sqlite` on the
   first request.

**Render** (permanent URL): New -> Blueprint -> pick the repo. `render.yaml`
selects the Docker runtime and `Dockerfile` installs PHP 8.3 + Apache with
`pdo_sqlite` and `pdo_mysql`.

Render has no native PHP runtime, so Docker is required.

**Caveat:** a free-tier filesystem is ephemeral, so records added through the UI
reset when the instance restarts. Seed data always returns. Point `config/db.php`
at a hosted MySQL for durable storage.

## Demo accounts

| Role | Email | Password |
|---|---|---|
| Owner | `ragav.owner@rentease.in` | `rent@1234` |
| Owner | `meera.owner@rentease.in` | `rent@1234` |
| Tenant | `arjun.tenant@rentease.in` | `rent@1234` |
| Tenant | `divya.tenant@rentease.in` | `rent@1234` |
| Tenant | `karthik.tenant@rentease.in` | `rent@1234` |
