-- ============================================================
--  RentEase : Rental Property Management System
--  Database : MySQL 8 / 9
--  File     : database/rentease.sql
-- ============================================================

DROP DATABASE IF EXISTS rentease;
CREATE DATABASE rentease
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE rentease;

-- ------------------------------------------------------------
-- 1. USERS : owners and tenants share one login table
-- ------------------------------------------------------------
CREATE TABLE users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(80)  NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    phone         VARCHAR(15)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('owner','tenant') NOT NULL DEFAULT 'tenant',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 2. PROPERTY LISTINGS
-- ------------------------------------------------------------
CREATE TABLE properties (
    property_id   INT AUTO_INCREMENT PRIMARY KEY,
    owner_id      INT NOT NULL,
    title         VARCHAR(120) NOT NULL,
    description   TEXT,
    property_type ENUM('Apartment','Independent House','Villa','PG / Hostel','Studio') NOT NULL,
    bhk           TINYINT NOT NULL,
    city          VARCHAR(60) NOT NULL,
    locality      VARCHAR(80) NOT NULL,
    address       VARCHAR(200) NOT NULL,
    rent_amount   DECIMAL(10,2) NOT NULL,
    deposit       DECIMAL(10,2) NOT NULL DEFAULT 0,
    area_sqft     INT NOT NULL,
    furnishing    ENUM('Unfurnished','Semi-Furnished','Fully-Furnished') NOT NULL,
    available_from DATE NOT NULL,
    status        ENUM('available','occupied','inactive') NOT NULL DEFAULT 'available',
    cover_image   VARCHAR(200),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_prop_owner FOREIGN KEY (owner_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_city     (city),
    INDEX idx_rent     (rent_amount),
    INDEX idx_bhk      (bhk),
    INDEX idx_status   (status)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 3. PROPERTY IMAGE GALLERY  (one row per image)
-- ------------------------------------------------------------
CREATE TABLE property_images (
    image_id    INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    image_path  VARCHAR(200) NOT NULL,
    caption     VARCHAR(120),
    CONSTRAINT fk_img_prop FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 4. RENTAL APPLICATIONS
-- ------------------------------------------------------------
CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id    INT NOT NULL,
    tenant_id      INT NOT NULL,
    message        TEXT,
    occupation     VARCHAR(60),
    family_size    TINYINT DEFAULT 1,
    applied_on     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status         ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending',
    UNIQUE KEY uq_app (property_id, tenant_id),
    CONSTRAINT fk_app_prop   FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE,
    CONSTRAINT fk_app_tenant FOREIGN KEY (tenant_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 5. RENT PAYMENT RECORDS
-- ------------------------------------------------------------
CREATE TABLE payments (
    payment_id  INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    tenant_id   INT NOT NULL,
    amount      DECIMAL(10,2) NOT NULL,
    pay_month   DATE NOT NULL,               -- always the 1st of the month
    method      ENUM('UPI','Net Banking','Card','Cash') NOT NULL,
    txn_ref     VARCHAR(40) NOT NULL,
    paid_on     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_pay (property_id, tenant_id, pay_month),
    CONSTRAINT fk_pay_prop   FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE,
    CONSTRAINT fk_pay_tenant FOREIGN KEY (tenant_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 6. MAINTENANCE COMPLAINTS
-- ------------------------------------------------------------
CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id  INT NOT NULL,
    tenant_id    INT NOT NULL,
    category     ENUM('Plumbing','Electrical','Carpentry','Appliance','Cleaning','Other') NOT NULL,
    subject      VARCHAR(120) NOT NULL,
    description  TEXT NOT NULL,
    priority     ENUM('Low','Medium','High') NOT NULL DEFAULT 'Medium',
    status       ENUM('open','in-progress','resolved') NOT NULL DEFAULT 'open',
    owner_note   VARCHAR(255),
    raised_on    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_on  DATETIME NULL,
    CONSTRAINT fk_cmp_prop   FOREIGN KEY (property_id)
        REFERENCES properties(property_id) ON DELETE CASCADE,
    CONSTRAINT fk_cmp_tenant FOREIGN KEY (tenant_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
--  SEED DATA
--  All passwords below are the plain string  rent@1234
--  (hashed at insert time with the same password_hash() call
--   used by register.php, see scripts/seed_hashes.php)
-- ============================================================

INSERT INTO users (full_name, email, phone, password_hash, role) VALUES
('Ragav Srinivasan','ragav.owner@rentease.in','9840012345','$2y$12$Gx1Nrxksz4PsCoHaLPY99e2nNt8VZi2O.ih0MlGUQwxBikMgbztJ2','owner'),
('Meera Krishnan',  'meera.owner@rentease.in','9840023456','$2y$12$Gx1Nrxksz4PsCoHaLPY99e2nNt8VZi2O.ih0MlGUQwxBikMgbztJ2','owner'),
('Arjun Nair',      'arjun.tenant@rentease.in','9840034567','$2y$12$Gx1Nrxksz4PsCoHaLPY99e2nNt8VZi2O.ih0MlGUQwxBikMgbztJ2','tenant'),
('Divya Raman',     'divya.tenant@rentease.in','9840045678','$2y$12$Gx1Nrxksz4PsCoHaLPY99e2nNt8VZi2O.ih0MlGUQwxBikMgbztJ2','tenant'),
('Karthik Vel',     'karthik.tenant@rentease.in','9840056789','$2y$12$Gx1Nrxksz4PsCoHaLPY99e2nNt8VZi2O.ih0MlGUQwxBikMgbztJ2','tenant');

INSERT INTO properties
(owner_id, title, description, property_type, bhk, city, locality, address,
 rent_amount, deposit, area_sqft, furnishing, available_from, status, cover_image) VALUES
(1,'Spacious 2 BHK near Peelamedu Tech Park',
 'Well-ventilated second-floor apartment with covered car parking, 24x7 water and power backup. Walkable to PSG Tech and Peelamedu bus stand.',
 'Apartment',2,'Coimbatore','Peelamedu','14/3, Anna Nagar Main Road, Peelamedu',
 16500.00,50000.00,980,'Semi-Furnished','2026-11-05','occupied','assets/properties/peelamedu-2bhk.jpg'),

(1,'Premium 3 BHK Villa with Private Garden',
 'Independent villa in a gated community with landscaped garden, modular kitchen and solar water heater. Ideal for families.',
 'Villa',3,'Coimbatore','Saravanampatti','Plot 27, Green Meadows, Saravanampatti',
 32000.00,100000.00,1750,'Fully-Furnished','2026-11-12','available','assets/properties/villa-3bhk.jpg'),

(2,'Budget 1 BHK for Working Professionals',
 'Compact 1 BHK on the ground floor with separate entrance, attached bathroom and two-wheeler parking. Water and EB included.',
 'Independent House',1,'Coimbatore','Saibaba Colony','8, Bharathi Street, Saibaba Colony',
 9500.00,25000.00,520,'Unfurnished','2026-11-01','occupied','assets/properties/saibaba-1bhk.jpg'),

(2,'Furnished Studio near Gandhipuram Bus Stand',
 'Fully furnished studio with AC, wardrobe, cot and kitchenette. Zero brokerage. Suitable for single working professionals.',
 'Studio',1,'Coimbatore','Gandhipuram','2nd Floor, Cross Cut Road, Gandhipuram',
 11000.00,30000.00,410,'Fully-Furnished','2026-11-08','available','assets/properties/studio-gandhipuram.jpg'),

(1,'3 BHK Apartment with Lake View',
 'East-facing apartment overlooking the lake, with clubhouse, gym and swimming pool access. Two covered parking slots.',
 'Apartment',3,'Chennai','Velachery','B-704, Lake Vista Apartments, Velachery',
 38000.00,120000.00,1620,'Semi-Furnished','2026-12-01','available','assets/properties/velachery-3bhk.jpg'),

(2,'Shared PG Room for Students',
 'Triple-sharing PG room with attached bath, meals and Wi-Fi included. Five minutes walk to Anna University campus.',
 'PG / Hostel',1,'Chennai','Guindy','23, Sardar Patel Road, Guindy',
 7500.00,15000.00,300,'Fully-Furnished','2026-11-03','available','assets/properties/pg-guindy.jpg'),

(1,'2 BHK Independent House with Terrace',
 'Independent house with private terrace, borewell plus corporation water and a small pooja room. Family preferred.',
 'Independent House',2,'Coimbatore','Vadavalli','41, Marudhamalai Road, Vadavalli',
 14000.00,42000.00,860,'Semi-Furnished','2026-11-20','available','assets/properties/vadavalli-2bhk.jpg'),

(2,'Sea-Facing 2 BHK Apartment',
 'Second-floor apartment with a sea-facing balcony, lift, generator backup and covered parking. Close to Elliot Beach.',
 'Apartment',2,'Chennai','Besant Nagar','5C, Elliot Residency, Besant Nagar',
 27500.00,80000.00,1150,'Fully-Furnished','2026-11-15','available','assets/properties/besant-2bhk.jpg');

INSERT INTO property_images (property_id, image_path, caption) VALUES
(1,'assets/properties/peelamedu-2bhk.jpg','Living room'),
(1,'assets/properties/peelamedu-kitchen.jpg','Modular kitchen'),
(1,'assets/properties/saibaba-bedroom.jpg','Bedroom with wardrobe'),
(2,'assets/properties/villa-3bhk.jpg','Front elevation'),
(3,'assets/properties/saibaba-1bhk.jpg','Bedroom'),
(4,'assets/properties/studio-gandhipuram.jpg','Studio interior'),
(5,'assets/properties/velachery-3bhk.jpg','Living area'),
(6,'assets/properties/pg-guindy.jpg','Sharing room'),
(7,'assets/properties/vadavalli-2bhk.jpg','Terrace view'),
(8,'assets/properties/besant-2bhk.jpg','Living area'),
(8,'assets/properties/besant-balcony.jpg','Sea-facing balcony');

INSERT INTO applications
(property_id, tenant_id, message, occupation, family_size, applied_on, status) VALUES
(1,3,'I am relocating to Coimbatore next month for work and would like to visit the flat this weekend.','Software Engineer',1,'2026-10-18 10:24:00','approved'),
(3,4,'Looking for a compact independent house close to my office. Can move in immediately.','Bank Officer',3,'2026-10-20 16:05:00','approved'),
(2,5,'Interested in the villa for my family of four. Please share the maintenance details.','Business Owner',4,'2026-10-25 09:40:00','pending'),
(5,3,'Relocating to Chennai in December. Kindly consider my application.','Software Engineer',1,'2026-10-27 11:15:00','pending'),
(8,4,'We are a family of three looking for a long-term rental near the beach.','Bank Officer',3,'2026-10-28 18:30:00','rejected');

INSERT INTO payments (property_id, tenant_id, amount, pay_month, method, txn_ref, paid_on) VALUES
(1,3,16500.00,'2026-08-01','UPI',       'UPI202608011002','2026-08-03 09:12:00'),
(1,3,16500.00,'2026-09-01','UPI',       'UPI202609011045','2026-09-02 10:31:00'),
(1,3,16500.00,'2026-10-01','Net Banking','NEFT202610011201','2026-10-01 12:05:00'),
(1,3,16500.00,'2026-11-01','UPI',       'UPI202611010908','2026-11-01 08:44:00'),
(3,4, 9500.00,'2026-09-01','Card',      'CARD202609011810','2026-09-01 18:10:00'),
(3,4, 9500.00,'2026-10-01','Card',      'CARD202610012015','2026-10-02 20:15:00'),
(3,4, 9500.00,'2026-11-01','UPI',       'UPI202611011133','2026-11-01 11:33:00');

INSERT INTO complaints
(property_id, tenant_id, category, subject, description, priority, status, owner_note, raised_on, resolved_on) VALUES
(1,3,'Plumbing','Kitchen tap leaking continuously',
 'The kitchen sink tap has been dripping for three days and the drain under the sink collects water.','High','resolved',
 'Plumber visited on 22nd, washer replaced and drain cleaned.','2026-10-20 08:15:00','2026-10-22 17:40:00'),
(1,3,'Electrical','Bedroom fan making noise',
 'The fan regulator in the second bedroom buzzes at low speed and the fan vibrates.','Medium','in-progress',
 'Electrician scheduled for Saturday morning.','2026-10-29 19:05:00',NULL),
(3,4,'Appliance','Geyser not heating',
 'The bathroom geyser trips the MCB after ten minutes of use.','High','open',
 NULL,'2026-10-31 07:50:00',NULL),
(3,4,'Cleaning','Common staircase needs cleaning',
 'The staircase between the ground and first floor has not been swept this week.','Low','open',
 NULL,'2026-11-01 09:30:00',NULL);
