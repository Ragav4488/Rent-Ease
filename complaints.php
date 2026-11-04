<?php
/**
 * RentEase – complaints.php
 * Tenant raises a maintenance complaint and sees the status track of every ticket.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('tenant');

$uid = (int) current_user()['user_id'];

$rentals = db()->prepare(
    'SELECT p.property_id, p.title
       FROM applications a
       JOIN properties p ON p.property_id = a.property_id
      WHERE a.tenant_id = ? AND a.status = "approved"
      ORDER BY p.title'
);
$rentals->execute([$uid]);
$rentals = $rentals->fetchAll();

$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $propId  = (int) ($_POST['property_id'] ?? 0);
    $cat     = $_POST['category'] ?? 'Other';
    $subject = trim($_POST['subject'] ?? '');
    $desc    = trim($_POST['description'] ?? '');
    $prio    = $_POST['priority'] ?? 'Medium';

    $allowedProps = array_map(fn($r) => (int) $r['property_id'], $rentals);

    if (!in_array($propId, $allowedProps, true)) {
        $errors[] = 'Choose one of your approved properties.';
    }
    if (mb_strlen($subject) < 6) {
        $errors[] = 'Subject must be at least 6 characters.';
    }
    if (mb_strlen($desc) < 15) {
        $errors[] = 'Please describe the problem in at least 15 characters.';
    }

    if (!$errors) {
        $ins = db()->prepare(
            'INSERT INTO complaints (property_id, tenant_id, category, subject, description, priority)
             VALUES (?, ?, ?, ?, ?, ?)'
        );
        $ins->execute([$propId, $uid, $cat, $subject, $desc, $prio]);
        flash('Complaint #RE' . str_pad((string) db()->lastInsertId(), 4, '0', STR_PAD_LEFT)
              . ' raised. The owner has been notified.');
        redirect('complaints.php');
    }
}

$list = db()->prepare(
    'SELECT c.*, p.title
       FROM complaints c
       JOIN properties p ON p.property_id = c.property_id
      WHERE c.tenant_id = ?
      ORDER BY c.raised_on DESC'
);
$list->execute([$uid]);
$list = $list->fetchAll();

$pageTitle = 'Maintenance complaints';
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.8rem">
  <div class="wrap">
    <p class="muted"><a href="tenant_dashboard.php">← Back to dashboard</a></p>
    <h1>Maintenance complaints</h1>

    <div class="detail" style="grid-template-columns:1fr 1.25fr">

      <!-- ---------- raise form ---------- -->
      <div class="panel" style="margin:0">
        <h2 style="font-size:1.1rem">Raise a new complaint</h2>

        <?php if (!$rentals): ?>
          <p class="muted">You need an approved rental before you can raise a complaint.</p>
          <a class="btn btn-block" href="properties.php">Browse properties</a>
        <?php else: ?>
          <?php if ($errors): ?>
            <div class="flash flash-error">
              <ul style="margin:0;padding-left:1.1rem">
                <?php foreach ($errors as $err): ?><li><?= e($err) ?></li><?php endforeach; ?>
              </ul>
            </div>
          <?php endif; ?>

          <form method="post" action="complaints.php" data-validate>
            <?= csrf_field() ?>

            <div class="field" style="margin-bottom:.8rem">
              <label for="property_id">Property</label>
              <select id="property_id" name="property_id" required>
                <?php foreach ($rentals as $r): ?>
                  <option value="<?= (int) $r['property_id'] ?>"><?= e($r['title']) ?></option>
                <?php endforeach; ?>
              </select>
            </div>

            <div class="form-grid" style="grid-template-columns:1fr 1fr">
              <div class="field">
                <label for="category">Category</label>
                <select id="category" name="category">
                  <?php foreach (['Plumbing','Electrical','Carpentry','Appliance','Cleaning','Other'] as $cat): ?>
                    <option value="<?= $cat ?>"><?= $cat ?></option>
                  <?php endforeach; ?>
                </select>
              </div>
              <div class="field">
                <label for="priority">Priority</label>
                <select id="priority" name="priority">
                  <option value="Low">Low</option>
                  <option value="Medium" selected>Medium</option>
                  <option value="High">High</option>
                </select>
              </div>
            </div>

            <div class="field" style="margin:.8rem 0">
              <label for="subject">Subject</label>
              <input type="text" id="subject" name="subject" maxlength="120"
                     value="<?= old('subject') ?>" placeholder="e.g. Kitchen tap leaking" required>
            </div>

            <div class="field" style="margin-bottom:.9rem">
              <label for="description">Describe the problem</label>
              <textarea id="description" name="description" rows="4" required
                        placeholder="When did it start, which room, and anything the owner should know…"><?= old('description') ?></textarea>
            </div>

            <button class="btn btn-block" type="submit">Submit complaint</button>
          </form>
        <?php endif; ?>
      </div>

      <!-- ---------- complaint history ---------- -->
      <div class="panel" style="margin:0">
        <h2 style="font-size:1.1rem">Complaint history</h2>

        <?php if (!$list): ?>
          <div class="empty"><strong>Nothing here yet</strong>
            Complaints you raise will appear in this list with live status.</div>
        <?php else: ?>
          <ul class="timeline">
            <?php foreach ($list as $c): ?>
              <li>
                <div style="display:flex;justify-content:space-between;gap:.6rem;align-items:start">
                  <strong><?= e($c['subject']) ?></strong>
                  <span class="<?= status_class($c['status']) ?>"><?= e($c['status']) ?></span>
                </div>
                <div class="when">
                  #RE<?= str_pad((string) $c['complaint_id'], 4, '0', STR_PAD_LEFT) ?>
                  · <?= e($c['category']) ?> · <?= e($c['priority']) ?> priority
                  · <?= e($c['title']) ?>
                </div>
                <p class="muted" style="margin:.35rem 0 0"><?= e($c['description']) ?></p>
                <?php if ($c['owner_note']): ?>
                  <p style="margin:.4rem 0 0;font-size:.86rem;background:var(--brand-tint);
                            padding:.5rem .7rem;border-radius:8px">
                    <strong>Owner:</strong> <?= e($c['owner_note']) ?>
                  </p>
                <?php endif; ?>
                <div class="when" style="margin-top:.3rem">
                  Raised <?= date('d M Y', strtotime($c['raised_on'])) ?>
                  <?= $c['resolved_on'] ? '· Resolved ' . date('d M Y', strtotime($c['resolved_on'])) : '' ?>
                </div>
              </li>
            <?php endforeach; ?>
          </ul>
        <?php endif; ?>
      </div>

    </div>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
