<?php
/**
 * RentEase – tenant_dashboard.php
 * Tenant home: applications, rent history, complaints and dues at a glance.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('tenant');

$uid = (int) current_user()['user_id'];

$apps = db()->prepare(
    'SELECT a.*, p.title, p.rent_amount, p.city, p.locality, p.cover_image
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.tenant_id = ?
      ORDER BY a.applied_on DESC'
);
$apps->execute([$uid]);
$apps = $apps->fetchAll();

$pays = db()->prepare(
    'SELECT pay.*, p.title
       FROM payments pay
       JOIN properties p ON p.property_id = pay.property_id
      WHERE pay.tenant_id = ?
      ORDER BY pay.pay_month DESC'
);
$pays->execute([$uid]);
$pays = $pays->fetchAll();

$cmps = db()->prepare(
    'SELECT c.*, p.title
       FROM complaints c
       JOIN properties p ON p.property_id = c.property_id
      WHERE c.tenant_id = ?
      ORDER BY c.raised_on DESC'
);
$cmps->execute([$uid]);
$cmps = $cmps->fetchAll();

$approved = array_values(array_filter($apps, fn($a) => $a['status'] === 'approved'));
$totalPaid = array_sum(array_column($pays, 'amount'));
$openCmps  = count(array_filter($cmps, fn($c) => $c['status'] !== 'resolved'));

$pageTitle = 'Tenant dashboard';
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.8rem">
  <div class="wrap">

    <div class="section-head">
      <div>
        <h1 style="margin-bottom:.2rem">Hello, <?= e(current_user()['full_name']) ?> 👋</h1>
        <p class="muted" style="margin:0">Here is everything about your rentals in one place.</p>
      </div>
      <a class="btn" href="properties.php">Browse properties</a>
    </div>

    <div class="stats">
      <div class="stat">
        <div class="label">Active rentals</div>
        <div class="value"><?= count($approved) ?></div>
        <div class="sub">approved applications</div>
      </div>
      <div class="stat">
        <div class="label">Pending applications</div>
        <div class="value"><?= count(array_filter($apps, fn($a) => $a['status'] === 'pending')) ?></div>
        <div class="sub">awaiting owner review</div>
      </div>
      <div class="stat">
        <div class="label">Rent paid</div>
        <div class="value"><?= money($totalPaid) ?></div>
        <div class="sub">across <?= count($pays) ?> receipts</div>
      </div>
      <div class="stat">
        <div class="label">Open complaints</div>
        <div class="value"><?= $openCmps ?></div>
        <div class="sub">of <?= count($cmps) ?> raised in total</div>
      </div>
    </div>

    <!-- ============ applications ============ -->
    <div class="panel">
      <div class="panel-head">
        <h2>My rental applications</h2>
        <a href="properties.php" class="muted">Apply for another property →</a>
      </div>

      <?php if (!$apps): ?>
        <div class="empty">
          <strong>No applications yet</strong>
          Browse the listings and submit your first rental application.
        </div>
      <?php else: ?>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Property</th><th>Location</th><th class="num">Rent</th>
                <th>Applied on</th><th>Status</th><th>Action</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($apps as $a): ?>
                <tr>
                  <td><a href="property.php?id=<?= (int) $a['property_id'] ?>"><?= e($a['title']) ?></a></td>
                  <td><?= e($a['locality']) ?>, <?= e($a['city']) ?></td>
                  <td class="num"><?= money($a['rent_amount']) ?></td>
                  <td><?= date('d M Y', strtotime($a['applied_on'])) ?></td>
                  <td><span class="<?= status_class($a['status']) ?>"><?= e($a['status']) ?></span></td>
                  <td>
                    <a class="btn btn-ghost btn-sm" href="property.php?id=<?= (int) $a['property_id'] ?>">View</a>
                  </td>
                </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      <?php endif; ?>
    </div>

    <!-- ============ payments ============ -->
    <div class="panel">
      <div class="panel-head">
        <h2>Rent payment records</h2>
        <?php if ($approved): ?>
          <a class="btn btn-sm" href="pay_rent.php">Pay rent</a>
        <?php endif; ?>
      </div>

      <?php if (!$pays): ?>
        <div class="empty">
          <strong>No payments recorded</strong>
          Once an application is approved you can record monthly rent here.
        </div>
      <?php else: ?>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Receipt #</th><th>Property</th><th>Month</th>
                <th class="num">Amount</th><th>Method</th><th>Transaction ref</th><th>Paid on</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($pays as $pay): ?>
                <tr>
                  <td>#PE<?= str_pad((string) $pay['payment_id'], 5, '0', STR_PAD_LEFT) ?></td>
                  <td><?= e($pay['title']) ?></td>
                  <td><?= month_label($pay['pay_month']) ?></td>
                  <td class="num"><?= money($pay['amount']) ?></td>
                  <td><?= e($pay['method']) ?></td>
                  <td><code style="font-size:.8rem"><?= e($pay['txn_ref']) ?></code></td>
                  <td><?= date('d M Y', strtotime($pay['paid_on'])) ?></td>
                </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      <?php endif; ?>
    </div>

    <!-- ============ complaints ============ -->
    <div class="panel">
      <div class="panel-head">
        <h2>My maintenance complaints</h2>
        <?php if ($approved): ?>
          <a class="btn btn-sm" href="complaints.php">Raise a complaint</a>
        <?php endif; ?>
      </div>

      <?php if (!$cmps): ?>
        <div class="empty">
          <strong>No complaints raised</strong>
          Something not working? Raise a maintenance complaint and the owner will be notified.
        </div>
      <?php else: ?>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Property</th><th>Category</th><th>Subject</th>
                <th>Priority</th><th>Raised on</th><th>Status</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($cmps as $c): ?>
                <tr>
                  <td><?= e($c['title']) ?></td>
                  <td><?= e($c['category']) ?></td>
                  <td><?= e($c['subject']) ?></td>
                  <td><span class="<?= $c['priority'] === 'High' ? 'chip chip-red'
                        : ($c['priority'] === 'Medium' ? 'chip chip-amber' : 'chip chip-blue') ?>">
                        <?= e($c['priority']) ?></span></td>
                  <td><?= date('d M Y', strtotime($c['raised_on'])) ?></td>
                  <td><span class="<?= status_class($c['status']) ?>"><?= e($c['status']) ?></span></td>
                </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      <?php endif; ?>
    </div>

  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
