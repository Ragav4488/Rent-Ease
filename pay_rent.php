<?php
/**
 * RentEase – pay_rent.php
 * Records a monthly rent payment for a property whose application was approved.
 * A UNIQUE(property_id, tenant_id, pay_month) key in MySQL prevents duplicates.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('tenant');

$uid = (int) current_user()['user_id'];

/* only approved rentals can receive a payment */
$rentals = db()->prepare(
    'SELECT p.property_id, p.title, p.rent_amount, p.deposit
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.tenant_id = ? AND a.status = "approved"
      ORDER BY p.title'
);
$rentals->execute([$uid]);
$rentals = $rentals->fetchAll();

$paidMonths = [];
if ($rentals) {
    $s = db()->prepare('SELECT property_id, pay_month FROM payments WHERE tenant_id = ?');
    $s->execute([$uid]);
    foreach ($s->fetchAll() as $row) {
        $paidMonths[$row['property_id']][] = $row['pay_month'];
    }
}

$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $propId = (int) ($_POST['property_id'] ?? 0);
    $month  = ($_POST['pay_month'] ?? '') . '-01';
    $method = $_POST['method'] ?? 'UPI';
    $txn    = trim($_POST['txn_ref'] ?? '');

    $validProps = array_column($rentals, 'property_id');

    if (!in_array($propId, array_map('intval', $validProps), true)) {
        $errors[] = 'Select a property you are approved for.';
    }
    if (!preg_match('/^\d{4}-\d{2}$/', $_POST['pay_month'] ?? '')) {
        $errors[] = 'Choose the month you are paying for.';
    }
    if (strlen($txn) < 6) {
        $errors[] = 'Enter a valid transaction reference (min 6 characters).';
    }
    if (!in_array($method, ['UPI', 'Net Banking', 'Card', 'Cash'], true)) {
        $errors[] = 'Choose a valid payment method.';
    }

    if (!$errors) {
        $amount = 0.0;
        foreach ($rentals as $r) {
            if ((int) $r['property_id'] === $propId) {
                $amount = (float) $r['rent_amount'];
            }
        }
        try {
            $ins = db()->prepare(
                'INSERT INTO payments (property_id, tenant_id, amount, pay_month, method, txn_ref)
                 VALUES (?, ?, ?, ?, ?, ?)'
            );
            $ins->execute([$propId, $uid, $amount, $month, $method, $txn]);
            flash('Rent of ' . money($amount) . ' recorded for ' . month_label($month) . '.');
            redirect('tenant_dashboard.php');
        } catch (PDOException $ex) {
            $errors[] = 'Rent for that month has already been recorded.';
        }
    }
}

/* default values for the form */
$defaultProp = (int) ($_POST['property_id'] ?? ($rentals[0]['property_id'] ?? 0));
$defaultRent = 0.0;
foreach ($rentals as $r) {
    if ((int) $r['property_id'] === $defaultProp) {
        $defaultRent = (float) $r['rent_amount'];
    }
}

$pageTitle = 'Pay rent';
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.8rem">
  <div class="wrap" style="max-width:760px">
    <p class="muted"><a href="tenant_dashboard.php">← Back to dashboard</a></p>
    <h1>Record a rent payment</h1>

    <?php if (!$rentals): ?>
      <div class="panel empty">
        <strong>No approved rentals</strong>
        Rent can be recorded only for a property whose application the owner approved.
        <p style="margin-top:1rem"><a class="btn" href="properties.php">Browse properties</a></p>
      </div>
    <?php else: ?>

      <?php if ($errors): ?>
        <div class="flash flash-error">
          <ul style="margin:0;padding-left:1.1rem">
            <?php foreach ($errors as $err): ?><li><?= e($err) ?></li><?php endforeach; ?>
          </ul>
        </div>
      <?php endif; ?>

      <form class="panel" method="post" action="pay_rent.php" data-validate>
        <?= csrf_field() ?>

        <div class="form-grid">
          <div class="field full">
            <label for="property_id">Property</label>
            <select id="property_id" name="property_id" required>
              <?php foreach ($rentals as $r): ?>
                <option value="<?= (int) $r['property_id'] ?>"
                        <?= (int) $r['property_id'] === $defaultProp ? 'selected' : '' ?>>
                  <?= e($r['title']) ?> — <?= money($r['rent_amount']) ?>/mo
                </option>
              <?php endforeach; ?>
            </select>
          </div>

          <div class="field">
            <label for="rent_amount">Monthly rent</label>
            <input type="text" id="rent_amount" name="rent_amount"
                   value="<?= money($defaultRent) ?>" readonly>
            <div class="hint">Three-month deposit:
              <strong id="depositPreview"><?= money($defaultRent * 3) ?></strong></div>
          </div>

          <div class="field">
            <label for="pay_month">Month being paid</label>
            <input type="month" id="pay_month" name="pay_month"
                   value="<?= e($_POST['pay_month'] ?? date('Y-m')) ?>" required>
          </div>

          <div class="field">
            <label for="method">Payment method</label>
            <select id="method" name="method" required>
              <?php foreach (['UPI', 'Net Banking', 'Card', 'Cash'] as $m): ?>
                <option value="<?= $m ?>" <?= ($_POST['method'] ?? '') === $m ? 'selected' : '' ?>>
                  <?= $m ?></option>
              <?php endforeach; ?>
            </select>
          </div>

          <div class="field">
            <label for="txn_ref">Transaction reference</label>
            <input type="text" id="txn_ref" name="txn_ref" maxlength="40"
                   value="<?= old('txn_ref') ?>" placeholder="e.g. UPI202611010908" required>
            <div class="hint">The UPI / NEFT / card reference from your bank statement.</div>
          </div>
        </div>

        <p class="muted" style="margin-top:1rem">
          The amount is taken from the property record, so it always matches the agreed rent.
        </p>

        <button class="btn" type="submit" style="margin-top:.6rem">Confirm payment</button>
        <a class="btn btn-ghost" href="tenant_dashboard.php">Cancel</a>
      </form>

      <div class="panel">
        <h2 style="font-size:1.05rem">Already paid for these months</h2>
        <ul style="margin:0;padding-left:1.1rem">
          <?php foreach ($rentals as $r): ?>
            <?php $months = $paidMonths[$r['property_id']] ?? []; ?>
            <li style="margin-bottom:.3rem">
              <strong><?= e($r['title']) ?></strong> —
              <?= $months ? implode(', ', array_map('month_label', $months)) : 'no payments yet' ?>
            </li>
          <?php endforeach; ?>
        </ul>
      </div>

    <?php endif; ?>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
