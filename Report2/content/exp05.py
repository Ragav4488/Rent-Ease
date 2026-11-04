from .. import theme


def build(doc):
    theme.exp_head(doc, "05", "05/08/2026",
                        "Event registration form using PHP and MySQL")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design a database-driven event registration form using HTML, PHP and "
                    "MySQL that stores participant details, rejects duplicate emails and lists "
                    "all registered participants.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Start Apache and MySQL from the XAMPP control panel.",
        "Create the database event_management and the table event_registrations.",
        "Create db.php to open a MySQLi connection and set the charset to utf8mb4.",
        "Design index.php with the participant name, email, mobile, institution, event "
        "name, category, number of participants and registration date.",
        "Submit the form to register.php using the POST method.",
        "Validate the input on the server: required fields, email format, mobile pattern.",
        "Check for an existing row with the same email before inserting.",
        "Insert the record with a prepared statement.",
        "Show a confirmation message, or the validation errors, on the same page.",
        "List every registration in participants.php with a SELECT query.",
        "Test with valid data, a bad email, an empty field and a duplicate email.",
    ])
    theme.heading_plain(doc, "DATABASE:")
    theme.code(doc, """CREATE DATABASE IF NOT EXISTS event_management;
USE event_management;

CREATE TABLE IF NOT EXISTS event_registrations (
    registration_id   INT AUTO_INCREMENT PRIMARY KEY,
    participant_name  VARCHAR(100) NOT NULL,
    email             VARCHAR(150) NOT NULL UNIQUE,
    mobile            VARCHAR(15)  NOT NULL,
    institution       VARCHAR(150) NOT NULL,
    event_name        VARCHAR(150) NOT NULL,
    category          VARCHAR(50)  NOT NULL,
    participants      INT          NOT NULL,
    registration_date DATE         NOT NULL
);""")
    theme.heading_plain(doc, "DB.PHP:")
    theme.code(doc, """<?php
$host     = "localhost";
$user     = "root";
$password = "YOUR_MYSQL_PASSWORD";
$database = "event_management";

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    error_log($conn->connect_error);
    die("Database connection failed.");
}

$conn->set_charset("utf8mb4");
?>""")
    theme.heading_plain(doc, "REGISTER.PHP:")
    theme.code(doc, """<?php
require_once 'db.php';

$errors = [];
$done   = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['participant_name'] ?? '');
    $mail = trim($_POST['email'] ?? '');
    $mob  = trim($_POST['mobile'] ?? '');
    $inst = trim($_POST['institution'] ?? '');
    $evnt = trim($_POST['event_name'] ?? '');
    $cat  = $_POST['category'] ?? '';
    $pax  = (int) ($_POST['participants'] ?? 0);
    $date = $_POST['registration_date'] ?? '';

    if ($name === '')                        $errors[] = 'Name is required.';
    if (!filter_var($mail, FILTER_VALIDATE_EMAIL)) $errors[] = 'Invalid email address.';
    if (!preg_match('/^[6-9]\\d{9}$/', $mob))      $errors[] = 'Invalid mobile number.';
    if ($pax < 1)                            $errors[] = 'Participants must be at least 1.';
    if ($date === '')                        $errors[] = 'Registration date is required.';

    if (!$errors) {
        $check = $conn->prepare('SELECT registration_id FROM event_registrations WHERE email = ?');
        $check->bind_param('s', $mail);
        $check->execute();
        if ($check->get_result()->fetch()) {
            $errors[] = 'This email is already registered.';
        }
    }

    if (!$errors) {
        $sql = 'INSERT INTO event_registrations
                  (participant_name, email, mobile, institution,
                   event_name, category, participants, registration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)';
        $stmt = $conn->prepare($sql);
        $stmt->bind_param('ssssssis', $name, $mail, $mob, $inst,
                          $evnt, $cat, $pax, $date);
        $stmt->execute();
        $done = true;
    }
}
?>""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "A valid registration shows a confirmation panel and the record appears in "
                    "participants.php. A duplicate email is refused with the message "
                    "\"This email is already registered.\"")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the event registration form was developed using HTML, PHP and MySQL "
                    "and duplicate registration was prevented with a unique email constraint.")
    theme.rubric_table(doc)
    theme.page_break(doc)
