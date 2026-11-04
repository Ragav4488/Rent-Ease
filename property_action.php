<?php
/**
 * RentEase – property_action.php
 * Owner toggles a listing between available and occupied.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('owner');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirect('owner_dashboard.php');
}
verify_csrf();

$propId = (int) ($_POST['property_id'] ?? 0);
$action = $_POST['action'] ?? '';

$check = db()->prepare('SELECT status FROM properties WHERE property_id = ? AND owner_id = ?');
$check->execute([$propId, current_user()['user_id']]);
$row = $check->fetch();

if (!$row) {
    flash('Property not found.', 'error');
    redirect('owner_dashboard.php');
}

if ($action === 'toggle_status') {
    $next = $row['status'] === 'available' ? 'occupied' : 'available';
    db()->prepare('UPDATE properties SET status = ? WHERE property_id = ?')
        ->execute([$next, $propId]);
    flash('Property marked as ' . $next . '.');
}

redirect('owner_dashboard.php');
