<?php
/**
 * RentEase – property.php : single listing + image gallery + apply form
 */
require_once __DIR__ . '/includes/functions.php';

$id = (int) ($_GET['id'] ?? 0);

$stmt = db()->prepare(
    'SELECT p.*, u.full_name AS owner_name, u.email AS owner_email, u.phone AS owner_phone
       FROM properties p
       JOIN users u ON u.user_id = p.owner_id
      WHERE p.property_id = ?'
);
$stmt->execute([$id]);
$p = $stmt->fetch();

if (!$p) {
    http_response_code(404);
    $pageTitle = 'Property not found';
    require __DIR__ . '/includes/header.php';
    echo '<div class="wrap"><div class="panel empty"><strong>404 – listing not found</strong>'
       . 'This property may have been removed.</div></div>';
    require __DIR__ . '/includes/footer.php';
    exit;
}

$images = db()->prepare('SELECT * FROM property_images WHERE property_id = ? ORDER BY image_id');
$images->execute([$id]);
$images = $images->fetchAll();
if (!$images) {
    $images = [['image_path' => $p['cover_image'], 'caption' => $p['title']]];
}

/* has the logged-in tenant already applied? */
$myApplication = null;
if (is_tenant()) {
    $s = db()->prepare('SELECT status, applied_on FROM applications WHERE property_id = ? AND tenant_id = ?');
    $s->execute([$id, current_user()['user_id']]);
    $myApplication = $s->fetch() ?: null;
}

$error = '';

/* ---- handle the rental application ---- */
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_login();
    if (!is_tenant()) {
        $error = 'Only tenant accounts can apply for a property.';
    } else {
        verify_csrf();
        $message    = trim($_POST['message'] ?? '');
        $occupation = trim($_POST['occupation'] ?? '');
        $family     = max(1, (int) ($_POST['family_size'] ?? 1));

        if ($myApplication) {
            $error = 'You have already applied for this property.';
        } elseif (mb_strlen($message) < 15) {
            $error = 'Please write at least 15 characters about yourself.';
        } elseif ($occupation === '') {
            $error = 'Please mention your occupation.';
        } else {
            $ins = db()->prepare(
                'INSERT INTO applications (property_id, tenant_id, message, occupation, family_size)
                 VALUES (?, ?, ?, ?, ?)'
            );
            $ins->execute([$id, current_user()['user_id'], $message, $occupation, $family]);

            flash('Application submitted. The owner will review it shortly.');
            redirect('property.php?id=' . $id);
        }
    }
}

$pageTitle = $p['title'];
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.6rem">
  <div class="wrap">
    <p class="muted" style="margin-bottom:.6rem">
      <a href="properties.php">← Back to all properties</a>
    </p>

    <div class="detail">

      <!-- ============ left column ============ -->
      <div>
        <div class="gallery-main">
          <img id="galleryMain" src="<?= e($images[0]['image_path']) ?>" alt="<?= e($p['title']) ?>">
        </div>

        <?php if (count($images) > 1): ?>
          <div class="gallery-thumbs">
            <?php foreach ($images as $i => $img): ?>
              <button type="button" class="<?= $i === 0 ? 'active' : '' ?>"
                      data-src="<?= e($img['image_path']) ?>"
                      title="<?= e($img['caption'] ?? '') ?>">
                <img src="<?= e($img['image_path']) ?>" alt="<?= e($img['caption'] ?? '') ?>">
              </button>
            <?php endforeach; ?>
          </div>
        <?php endif; ?>

        <div class="panel" style="margin-top:1.2rem">
          <div class="panel-head">
            <h2><?= e($p['title']) ?></h2>
            <span class="<?= status_class($p['status']) ?>"><?= e($p['status']) ?></span>
          </div>
          <p class="muted" style="margin-top:-.4rem">
            📍 <?= e($p['address']) ?>, <?= e($p['locality']) ?>, <?= e($p['city']) ?>
          </p>
          <p><?= nl2br(e($p['description'])) ?></p>

          <h3 style="margin-top:1.4rem">Specifications</h3>
          <ul class="spec-list">
            <li><span class="k">Property type</span><span><?= e($p['property_type']) ?></span></li>
            <li><span class="k">Bedrooms</span><span><?= (int) $p['bhk'] ?> BHK</span></li>
            <li><span class="k">Built-up area</span><span><?= (int) $p['area_sqft'] ?> sq.ft</span></li>
            <li><span class="k">Furnishing</span><span><?= e($p['furnishing']) ?></span></li>
            <li><span class="k">Monthly rent</span><span><?= money($p['rent_amount']) ?></span></li>
            <li><span class="k">Security deposit</span><span><?= money($p['deposit']) ?></span></li>
            <li><span class="k">Available from</span><span><?= date('d M Y', strtotime($p['available_from'])) ?></span></li>
            <li><span class="k">Listed by</span><span><?= e($p['owner_name']) ?></span></li>
          </ul>
        </div>
      </div>

      <!-- ============ right column ============ -->
      <aside>
        <div class="panel">
          <div style="display:flex;justify-content:space-between;align-items:baseline">
            <div>
              <div style="font-size:1.6rem;font-weight:700;color:var(--brand-dark)">
                <?= money($p['rent_amount']) ?>
              </div>
              <div class="muted">per month + <?= money($p['deposit']) ?> deposit</div>
            </div>
          </div>
          <hr style="border:none;border-top:1px solid var(--line);margin:1rem 0">
          <p class="muted" style="margin:0 0 .2rem">Owner</p>
          <p style="margin:0 0 .1rem"><strong><?= e($p['owner_name']) ?></strong></p>
          <p class="muted" style="margin:0">
            <?= e($p['owner_phone']) ?> · <?= e($p['owner_email']) ?>
          </p>
        </div>

        <div class="panel">
          <h2 style="font-size:1.05rem">Apply for this property</h2>

          <?php if ($error): ?>
            <div class="flash flash-error" style="margin-bottom:.9rem"><?= e($error) ?></div>
          <?php endif; ?>

          <?php if (!is_logged_in()): ?>
            <p class="muted">You need a tenant account to apply.</p>
            <a class="btn btn-block" href="login.php">Log in to apply</a>
            <p class="muted" style="text-align:center;margin:.7rem 0 0">
              New user? <a href="register.php">Register free</a>
            </p>

          <?php elseif (is_owner()): ?>
            <p class="muted">You are signed in as an owner. Owner accounts cannot
               submit rental applications.</p>
            <a class="btn btn-ghost btn-block" href="owner_dashboard.php">Go to owner dashboard</a>

          <?php elseif ($myApplication): ?>
            <div class="chip <?= $myApplication['status'] === 'approved' ? 'chip-green'
                                 : ($myApplication['status'] === 'rejected' ? 'chip-red' : 'chip-amber') ?>">
              Application <?= e($myApplication['status']) ?>
            </div>
            <p class="muted" style="margin-top:.7rem">
              You applied on <?= date('d M Y', strtotime($myApplication['applied_on'])) ?>.
            </p>
            <a class="btn btn-ghost btn-block" href="tenant_dashboard.php">View my applications</a>

          <?php else: ?>
            <form method="post" action="property.php?id=<?= $id ?>" data-validate>
              <?= csrf_field() ?>
              <div class="field" style="margin-bottom:.8rem">
                <label for="occupation">Occupation</label>
                <input type="text" id="occupation" name="occupation"
                       value="<?= old('occupation') ?>" placeholder="e.g. Software Engineer" required>
              </div>
              <div class="field" style="margin-bottom:.8rem">
                <label for="family_size">Family size</label>
                <input type="number" id="family_size" name="family_size" min="1" max="20"
                       value="<?= old('family_size', '1') ?>">
              </div>
              <div class="field" style="margin-bottom:.9rem">
                <label for="message">Message to the owner</label>
                <textarea id="message" name="message" rows="4" required
                          placeholder="Tell the owner a little about yourself and your move-in date…"><?= old('message') ?></textarea>
              </div>
              <button class="btn btn-block" type="submit">Submit application</button>
            </form>
          <?php endif; ?>
        </div>
      </aside>

    </div>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
