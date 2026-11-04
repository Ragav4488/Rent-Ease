<?php
/**
 * RentEase – application_action.php
 * Owner approves or rejects a pending rental application.
 * Approval also flips the property to "occupied".
 */
require_once __DIR__ . '/includes/functions.php';
require_role('owner');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirect('owner_dashboard.php');
}
verify_csrf();

$appId    = (int) ($_POST['application_id'] ?? 0);
$decision = $_POST['decision'] ?? '';

if (!in_array($decision, ['approved', 'rejected'], true)) {
    flash('Invalid decision.', 'error');
    redirect('owner_dashboard.php');
}

/* make sure this application belongs to one of THIS owner's properties */
$check = db()->prepare(
    'SELECT a.application_id, a.property_id, a.status, p.title
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.application_id = ? AND p.owner_id = ?'
);
$check->execute([$appId, current_user()['user_id']]);
$app = $check->fetch();

if (!$app) {
    flash('Application not found.', 'error');
    redirect('owner_dashboard.php');
}
if ($app['status'] !== 'pending') {
    flash('That application has already been decided.', 'error');
    redirect('owner_dashboard.php');
}

$pdo = db();
$pdo->beginTransaction();
try {
    $upd = $pdo->prepare('UPDATE applications SET status = ? WHERE application_id = ?');
    $upd->execute([$decision, $appId]);

    if ($decision === 'approved') {
        $pdo->prepare('UPDATE properties SET status = "occupied" WHERE property_id = ?')
            ->execute([$app['property_id']]);
        /* reject every other pending application for the same property */
        $pdo->prepare(
            'UPDATE applications SET status = "rejected"
              WHERE property_id = ? AND status = "pending" AND application_id <> ?'
        )->execute([$app['property_id'], $appId]);
    }

    $pdo->commit();
} catch (PDOException $ex) {
    $pdo->rollBack();
    flash('Could not update the application.', 'error');
    redirect('owner_dashboard.php');
}

flash($decision === 'approved'
    ? 'Application approved — "' . $app['title'] . '" is now marked occupied.'
    : 'Application rejected.');
redirect('owner_dashboard.php');
