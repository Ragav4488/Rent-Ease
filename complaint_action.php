<?php
/**
 * RentEase – complaint_action.php
 * Owner moves a complaint through open → in-progress → resolved and
 * leaves a note that the tenant sees on their dashboard.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('owner');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirect('owner_dashboard.php');
}
verify_csrf();

$cmpId  = (int) ($_POST['complaint_id'] ?? 0);
$status = $_POST['status'] ?? '';
$note   = trim($_POST['owner_note'] ?? '');

if (!in_array($status, ['open', 'in-progress', 'resolved'], true)) {
    flash('Invalid status.', 'error');
    redirect('owner_dashboard.php');
}

$check = db()->prepare(
    'SELECT c.complaint_id
       FROM complaints c
       JOIN properties p ON p.property_id = c.property_id
      WHERE c.complaint_id = ? AND p.owner_id = ?'
);
$check->execute([$cmpId, current_user()['user_id']]);
if (!$check->fetch()) {
    flash('Complaint not found.', 'error');
    redirect('owner_dashboard.php');
}

$stmt = db()->prepare(
    'UPDATE complaints
        SET status = ?,
            owner_note = ?,
            resolved_on = ' . ($status === 'resolved' ? 'NOW()' : 'NULL') . '
      WHERE complaint_id = ?'
);
$stmt->execute([$status, $note !== '' ? $note : null, $cmpId]);

flash('Complaint #RE' . str_pad((string) $cmpId, 4, '0', STR_PAD_LEFT)
      . ' updated to "' . $status . '".');
redirect('owner_dashboard.php');
