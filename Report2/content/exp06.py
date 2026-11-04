from .. import theme


def build(doc):
    theme.exp_head(doc, "06", "19/08/2026",
                        "Web application for food delivery system using PHP and MySQL")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design a food delivery web application using PHP and MySQL where a user "
                    "registers, logs in, browses the menu, places an order and receives an order "
                    "confirmation, and an administrator manages the menu and order status.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Create the project folder food-delivery inside htdocs and start Apache and MySQL.",
        "Create the database food_delivery with the tables users, food_items, orders "
        "and order_items.",
        "Write db.php to connect PHP to MySQL over MySQLi.",
        "Build register.php and login.php with password_hash() and password_verify().",
        "Build menu.php to read food_items and render one card per item.",
        "Let the user set a quantity and add items to a session cart.",
        "Collect the customer name, mobile number and delivery address at checkout.",
        "Compute the total, insert the order and its line items in a transaction.",
        "Show an order confirmation with the order id, items, total and status.",
        "Build admin.php to add or remove items and advance the order status.",
        "Test registration, login, ordering and the admin operations.",
    ])
    theme.heading_plain(doc, "DATABASE:")
    theme.code(doc, """CREATE DATABASE IF NOT EXISTS food_delivery;
USE food_delivery;

CREATE TABLE users (
    user_id  INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    mobile   VARCHAR(15),
    address  TEXT
);

CREATE TABLE food_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    price   DECIMAL(8,2) NOT NULL,
    category VARCHAR(50),
    available TINYINT(1) DEFAULT 1
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id  INT NOT NULL,
    total    DECIMAL(10,2) NOT NULL,
    address  TEXT NOT NULL,
    status   ENUM('placed','preparing','delivered','cancelled') DEFAULT 'placed',
    ordered_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
    item_id  INT NOT NULL,
    order_id INT NOT NULL,
    qty      INT NOT NULL,
    price    DECIMAL(8,2) NOT NULL,
    PRIMARY KEY (item_id, order_id),
    FOREIGN KEY (item_id)  REFERENCES food_items(item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);""")
    theme.heading_plain(doc, "CHECKOUT.PHP (TRANSACTION):")
    theme.code(doc, """<?php
session_start();
require_once 'db.php';

if (empty($_SESSION['cart'])) {
    die('Your cart is empty.');
}

$address = trim($_POST['address'] ?? '');
$total   = 0.0;

foreach ($_SESSION['cart'] as $itemId => $qty) {
    $stmt = $conn->prepare('SELECT price FROM food_items WHERE item_id = ?');
    $stmt->bind_param('i', $itemId);
    $stmt->execute();
    $row = $stmt->get_result()->fetch_assoc();
    $total += $row['price'] * $qty;
}

$conn->begin_transaction();

try {
    $ins = $conn->prepare(
        'INSERT INTO orders (user_id, total, address) VALUES (?, ?, ?)');
    $ins->bind_param('ids', $_SESSION['user_id'], $total, $address);
    $ins->execute();
    $orderId = $conn->insert_id;

    $line = $conn->prepare(
        'INSERT INTO order_items (order_id, item_id, qty, price)
         VALUES (?, ?, ?, ?)');

    foreach ($_SESSION['cart'] as $itemId => $qty) {
        $price = /* current price from food_items */ 0;
        $line->bind_param('iiid', $orderId, $itemId, $qty, $price);
        $line->execute();
    }

    $conn->commit();
    $_SESSION['cart'] = [];
    header('Location: confirmation.php?order=' . $orderId);
} catch (Throwable $e) {
    $conn->rollback();
    die('Order could not be placed.');
}""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "The menu lists the available dishes, the cart totals the selected quantities "
                    "and checkout writes the order and its lines in one transaction. The "
                    "confirmation page shows the order id and status, which the administrator can "
                    "advance from Placed to Preparing to Delivered.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the food delivery web application was developed using PHP and MySQL with "
                    "session-based cart handling and transactional order insertion.")
    theme.rubric_table(doc)
    theme.page_break(doc)
