<?php
/**
 * RentEase – owner_dashboard.php
 * Owner control centre: portfolio stats, listings, applications,
 * rent collection chart and the maintenance queue.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('owner');

$uid = (int) current_user()['user_id'];

/* ---- portfolio ---- */
$props = db()->prepare(
    'SELECT p.*,
            (SELECT COUNT(*) FROM applications a
              WHERE a.property_id = p.property_id AND a.status = "pending") AS pending_apps,
            (SELECT COUNT(*) FROM applications a
              WHERE a.property_id = p.property_id AND a.status = "approved") AS tenants
       FROM properties p
      WHERE p.owner_id = ?
      ORDER BY p.created_at DESC'
);
$props->execute([$uid]);
$props = $props->fetchAll();

/* ---- applications across all owned properties ---- */
$apps = db()->prepare(
    "SELECT a.*, p.title, u.full_name AS tenant_name, u.phone, u.email
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
       JOIN users u      ON u.user_id     = a.tenant_id
      WHERE p.owner_id = ?
      ORDER BY CASE a.status WHEN 'pending' THEN 0 WHEN 'approved' THEN 1 ELSE 2 END, a.applied_on DESC"
);
$apps->execute([$uid]);
$apps = $apps->fetchAll();

/* ---- rent collected per month (last 6 months) ---- */
$sixMonthsAgo = date('Y-m-01', strtotime('-5 months'));
$chart = db()->prepare(
    "SELECT SUBSTR(pay.pay_month, 1, 7) AS ym,
            SUM(pay.amount) AS total
       FROM payments pay
       JOIN properties p ON p.property_id = pay.property_id
      WHERE p.owner_id = ?
        AND pay.pay_month >= ?
      GROUP BY ym
      ORDER BY ym"
);
$chart->execute([$uid, $sixMonthsAgo]);
$chart = $chart->fetchAll();

/* ---- complaints on owned properties ---- */
$cmps = db()->prepare(
    "SELECT c.*, p.title, u.full_name AS tenant_name
       FROM complaints c
       JOIN properties p ON p.property_id = c.property_id
       JOIN users u      ON u.user_id     = c.tenant_id
      WHERE p.owner_id = ?
      ORDER BY CASE c.status WHEN 'open' THEN 0 WHEN 'in-progress' THEN 1 ELSE 2 END, c.raised_on DESC"
);
$cmps->execute([$uid]);
$cmps = $cmps->fetchAll();

$totalProps   = count($props);
$occupied     = count(array_filter($props, fn($p) => $p['status'] === 'occupied'));
$pendingCount = count(array_filter($apps, fn($a) => $a['status'] === 'pending'));
$openCmps     = count(array_filter($cmps, fn($c) => $c['status'] !== 'resolved'));

$collectedStmt = db()->prepare(
    'SELECT COALESCE(SUM(pay.amount),0)
       FROM payments pay
       JOIN properties p ON p.property_id = pay.property_id
      WHERE p.owner_id = ?'
);
$collectedStmt->execute([$uid]);
$collected = (float) $collectedStmt->fetchColumn();

$monthlyRent = array_sum(array_map(
    fn($p) => $p['status'] === 'occupied' ? (float) $p['rent_amount'] : 0.0,
    $props
));

$maxChart = max(1, ...array_map(fn($r) => (float) $r['total'], $chart ?: [['total' => 1]]));

$pageTitle = 'Owner dashboard';
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.8rem">
  <div class="wrap">

    <div class="section-head">
      <div>
        <h1 style="margin-bottom:.2rem">Owner dashboard</h1>
        <p class="muted" style="margin:0"><?= e(current_user()['full_name']) ?> ·
           <?= $totalProps ?> listings · <?= $pendingCount ?> applications waiting</p>
      </div>
      <a class="btn" href="add_property.php">+ Add property</a>
    </div>

    <div class="stats">
      <div class="stat">
        <div class="label">Listings</div>
        <div class="value"><?= $totalProps ?></div>
        <div class="sub"><?= $occupied ?> occupied · <?= $totalProps - $occupied ?> available</div>
      </div>
      <div class="stat">
        <div class="label">Rent collected</div>
        <div class="value"><?= money($collected) ?></div>
        <div class="sub">all months, all properties</div>
      </div>
      <div class="stat">
        <div class="label">Monthly rent roll</div>
        <div class="value"><?= money($monthlyRent) ?></div>
        <div class="sub">from occupied properties</div>
      </div>
      <div class="stat">
        <div class="label">Open complaints</div>
        <div class="value"><?= $openCmps ?></div>
        <div class="sub">of <?= count($cmps) ?> raised by tenants</div>
      </div>
    </div>

    <!-- ============ properties ============ -->
    <div class="panel">
      <div class="panel-head">
        <h2>My properties</h2>
        <a href="add_property.php" class="muted">Add a new listing →</a>
      </div>

      <?php if (!$props): ?>
        <div class="empty"><strong>No properties listed</strong>
          Add your first property to start receiving tenant applications.</div>
      <?php else: ?>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Property</th><th>Type</th><th>Location</th>
                <th class="num">Rent</th><th>Tenants</th><th>Status</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($props as $p): ?>
                <tr>
                  <td>
                    <a href="property.php?id=<?= (int) $p['property_id'] ?>"><?= e($p['title']) ?></a>
                    <?php if ($p['pending_apps']): ?>
                      <span class="chip chip-amber"><?= (int) $p['pending_apps'] ?> new</span>
                    <?php endif; ?>
                  </td>
                  <td><?= e($p['property_type']) ?> · <?= (int) $p['bhk'] ?> BHK</td>
                  <td><?= e($p['locality']) ?>, <?= e($p['city']) ?></td>
                  <td class="num"><?= money($p['rent_amount']) ?></td>
                  <td><?= (int) $p['tenants'] ?></td>
                  <td><span class="<?= status_class($p['status']) ?>"><?= e($p['status']) ?></span></td>
                  <td style="white-space:nowrap">
                    <form method="post" action="property_action.php" style="display:inline">
                      <?= csrf_field() ?>
                      <input type="hidden" name="property_id" value="<?= (int) $p['property_id'] ?>">
                      <input type="hidden" name="action" value="toggle_status">
                      <button class="btn btn-ghost btn-sm" type="submit">
                        <?= $p['status'] === 'available' ? 'Mark occupied' : 'Mark available' ?>
                      </button>
                    </form>
                  </td>
                </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      <?php endif; ?>
    </div>

    <!-- ============ rent chart ============ -->
    <div class="panel">
      <h2>Rent collected per month</h2>
      <?php if (!$chart): ?>
        <p class="muted">No rent recorded in the last six months.</p>
      <?php else: ?>
        <div style="display:flex;gap:1.1rem;align-items:flex-end;height:190px;padding:.5rem 0 0">
          <?php foreach ($chart as $row):
              $h = max(6, (int) round(((float) $row['total'] / $maxChart) * 150));
              $rowLabel = date('M Y', strtotime($row['ym'] . '-01'));
          ?>
            <div style="flex:1;text-align:center">
              <div style="font-size:.75rem;font-weight:700;color:var(--brand-dark);margin-bottom:.35rem">
                <?= money($row['total']) ?>
              </div>
              <div title="<?= e($rowLabel) ?>"
                   style="height:<?= $h ?>px;background:linear-gradient(180deg,#14b8a6,#0f766e);
                          border-radius:8px 8px 3px 3px"></div>
              <div class="muted" style="margin-top:.4rem;font-size:.76rem"><?= e($rowLabel) ?></div>
            </div>
          <?php endforeach; ?>
        </div>
      <?php endif; ?>
    </div>

    <!-- ============ applications ============ -->
    <div class="panel">
      <div class="panel-head">
        <h2>Rental applications</h2>
        <span class="muted"><?= $pendingCount ?> awaiting your decision</span>
      </div>

      <?php if (!$apps): ?>
        <div class="empty"><strong>No applications yet</strong>
          Verified tenants will appear here as soon as they apply.</div>
      <?php else: ?>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Tenant</th><th>Property</th><th>Occupation</th>
                <th class="num">Family</th><th>Applied</th><th>Status</th><th>Decision</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($apps as $a): ?>
                <tr>
                  <td>
                    <strong><?= e($a['tenant_name']) ?></strong><br>
                    <span class="muted"><?= e($a['phone']) ?></span>
                    <details style="margin-top:.25rem">
                      <summary class="muted" style="cursor:pointer">message</summary>
                      <p class="muted" style="margin:.3rem 0 0;max-width:320px"><?= e($a['message']) ?></p>
                    </details>
                  </td>
                  <td><?= e($a['title']) ?></td>
                  <td><?= e($a['occupation']) ?></td>
                  <td class="num"><?= (int) $a['family_size'] ?></td>
                  <td><?= date('d M Y', strtotime($a['applied_on'])) ?></td>
                  <td><span class="<?= status_class($a['status']) ?>"><?= e($a['status']) ?></span></td>
                  <td style="white-space:nowrap">
                    <?php if ($a['status'] === 'pending'): ?>
                      <form method="post" action="application_action.php" style="display:inline">
                        <?= csrf_field() ?>
                        <input type="hidden" name="application_id" value="<?= (int) $a['application_id'] ?>">
                        <button class="btn btn-sm" name="decision" value="approved">Approve</button>
                      </form>
                      <form method="post" action="application_action.php" style="display:inline">
                        <?= csrf_field() ?>
                        <input type="hidden" name="application_id" value="<?= (int) $a['application_id'] ?>">
                        <button class="btn btn-danger btn-sm" name="decision" value="rejected">Reject</button>
                      </form>
                    <?php else: ?>
                      <span class="muted">decided</span>
                    <?php endif; ?>
                  </td>
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
        <h2>Maintenance complaints</h2>
        <span class="muted"><?= $openCmps ?> unresolved</span>
      </div>

      <?php if (!$cmps): ?>
        <div class="empty"><strong>No complaints</strong> All quiet on the maintenance front.</div>
      <?php else: ?>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Tenant</th><th>Property</th><th>Category</th><th>Subject</th>
                <th>Priority</th><th>Raised</th><th>Status</th><th>Update</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($cmps as $c): ?>
                <tr>
                  <td><?= e($c['tenant_name']) ?></td>
                  <td><?= e($c['title']) ?></td>
                  <td><?= e($c['category']) ?></td>
                  <td style="max-width:260px"><?= e($c['subject']) ?></td>
                  <td><span class="<?= $c['priority'] === 'High' ? 'chip chip-red'
                        : ($c['priority'] === 'Medium' ? 'chip chip-amber' : 'chip chip-blue') ?>">
                        <?= e($c['priority']) ?></span></td>
                  <td><?= date('d M Y', strtotime($c['raised_on'])) ?></td>
                  <td><span class="<?= status_class($c['status']) ?>"><?= e($c['status']) ?></span></td>
                  <td style="white-space:nowrap">
                    <form method="post" action="complaint_action.php"
                          style="display:flex;gap:.35rem;align-items:center">
                      <?= csrf_field() ?>
                      <input type="hidden" name="complaint_id" value="<?= (int) $c['complaint_id'] ?>">
                      <select name="status" style="width:auto;padding:.3rem;font-size:.82rem">
                        <?php foreach (['open', 'in-progress', 'resolved'] as $s): ?>
                          <option value="<?= $s ?>" <?= $c['status'] === $s ? 'selected' : '' ?>>
                            <?= $s ?></option>
                        <?php endforeach; ?>
                      </select>
                      <input type="text" name="owner_note" placeholder="note" maxlength="255"
                             value="<?= e($c['owner_note']) ?>"
                             style="width:110px;padding:.3rem;font-size:.82rem">
                      <button class="btn btn-sm" type="submit">Save</button>
                    </form>
                  </td>
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
