<?php
/**
 * RentEase – add_property.php
 * Owner creates a listing. The cover image is uploaded with the same
 * validate-type-then-store pattern used by the lab's file-upload exercise.
 */
require_once __DIR__ . '/includes/functions.php';
require_role('owner');

$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $title    = trim($_POST['title'] ?? '');
    $desc     = trim($_POST['description'] ?? '');
    $type     = $_POST['property_type'] ?? 'Apartment';
    $bhk      = max(1, (int) ($_POST['bhk'] ?? 1));
    $city     = trim($_POST['city'] ?? '');
    $locality = trim($_POST['locality'] ?? '');
    $address  = trim($_POST['address'] ?? '');
    $rent     = (float) ($_POST['rent_amount'] ?? 0);
    $deposit  = (float) ($_POST['deposit'] ?? 0);
    $area     = (int) ($_POST['area_sqft'] ?? 0);
    $furnish  = $_POST['furnishing'] ?? 'Unfurnished';
    $avail    = $_POST['available_from'] ?? date('Y-m-d');

    if (mb_strlen($title) < 10)            $errors[] = 'Title must be at least 10 characters.';
    if ($city === '')                      $errors[] = 'City is required.';
    if ($locality === '')                  $errors[] = 'Locality is required.';
    if ($address === '')                   $errors[] = 'Full address is required.';
    if ($rent <= 0)                        $errors[] = 'Rent must be greater than zero.';
    if ($area <= 0)                        $errors[] = 'Built-up area must be greater than zero.';
    if (!in_array($type, ['Apartment','Independent House','Villa','PG / Hostel','Studio'], true))
        $errors[] = 'Choose a valid property type.';
    if (!in_array($furnish, ['Unfurnished','Semi-Furnished','Fully-Furnished'], true))
        $errors[] = 'Choose a valid furnishing option.';

    /* ---- cover image upload ---- */
    $coverImage = 'assets/properties/placeholder.jpg';
    if (!empty($_FILES['cover']['name'])) {
        $allowed = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'];
        $mime    = mime_content_type($_FILES['cover']['tmp_name']);

        if (!isset($allowed[$mime])) {
            $errors[] = 'Cover image must be a JPG, PNG or WEBP file.';
        } elseif ($_FILES['cover']['size'] > 2 * 1024 * 1024) {
            $errors[] = 'Cover image must be smaller than 2 MB.';
        } else {
            $name = 'p' . time() . '_' . bin2hex(random_bytes(4)) . '.' . $allowed[$mime];
            $dest = __DIR__ . '/assets/properties/' . $name;
            if (move_uploaded_file($_FILES['cover']['tmp_name'], $dest)) {
                $coverImage = 'assets/properties/' . $name;
            } else {
                $errors[] = 'Could not save the uploaded image.';
            }
        }
    }

    if (!$errors) {
        $pdo = db();
        $pdo->beginTransaction();
        try {
            $ins = $pdo->prepare(
                'INSERT INTO properties
                   (owner_id, title, description, property_type, bhk, city, locality, address,
                    rent_amount, deposit, area_sqft, furnishing, available_from, cover_image)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            );
            $ins->execute([
                current_user()['user_id'], $title, $desc, $type, $bhk, $city, $locality,
                $address, $rent, $deposit, $area, $furnish, $avail, $coverImage,
            ]);
            $newId = (int) $pdo->lastInsertId();

            $img = $pdo->prepare(
                'INSERT INTO property_images (property_id, image_path, caption) VALUES (?,?,?)'
            );
            $img->execute([$newId, $coverImage, 'Cover photo']);

            $pdo->commit();
            flash('Property "' . $title . '" published successfully.');
            redirect('property.php?id=' . $newId);
        } catch (PDOException $ex) {
            $pdo->rollBack();
            $errors[] = 'Could not save the property: ' . $ex->getMessage();
        }
    }
}

$pageTitle = 'Add a property';
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.8rem">
  <div class="wrap" style="max-width:860px">
    <p class="muted"><a href="owner_dashboard.php">← Back to dashboard</a></p>
    <h1>List a new property</h1>
    <p class="muted">Complete listings receive up to three times more applications.</p>

    <?php if ($errors): ?>
      <div class="flash flash-error">
        <ul style="margin:0;padding-left:1.1rem">
          <?php foreach ($errors as $err): ?><li><?= e($err) ?></li><?php endforeach; ?>
        </ul>
      </div>
    <?php endif; ?>

    <form class="panel" method="post" action="add_property.php"
          enctype="multipart/form-data" data-validate>
      <?= csrf_field() ?>

      <div class="form-grid">
        <div class="field full">
          <label for="title">Listing title</label>
          <input type="text" id="title" name="title" maxlength="120"
                 value="<?= old('title') ?>" placeholder="e.g. Spacious 2 BHK near Peelamedu Tech Park" required>
        </div>

        <div class="field">
          <label for="property_type">Property type</label>
          <select id="property_type" name="property_type">
            <?php foreach (['Apartment','Independent House','Villa','PG / Hostel','Studio'] as $t): ?>
              <option value="<?= $t ?>"><?= $t ?></option>
            <?php endforeach; ?>
          </select>
        </div>

        <div class="field">
          <label for="bhk">Bedrooms (BHK)</label>
          <input type="number" id="bhk" name="bhk" min="1" max="6" value="<?= old('bhk', '2') ?>">
        </div>

        <div class="field">
          <label for="city">City</label>
          <input type="text" id="city" name="city" value="<?= old('city') ?>" required>
        </div>

        <div class="field">
          <label for="locality">Locality</label>
          <input type="text" id="locality" name="locality" value="<?= old('locality') ?>" required>
        </div>

        <div class="field full">
          <label for="address">Full address</label>
          <input type="text" id="address" name="address" value="<?= old('address') ?>" required>
        </div>

        <div class="field">
          <label for="rent_amount">Monthly rent (₹)</label>
          <input type="number" id="rent_amount" name="rent_amount" min="0" step="100"
                 value="<?= old('rent_amount') ?>" required>
        </div>

        <div class="field">
          <label for="deposit">Security deposit (₹)</label>
          <input type="number" id="deposit" name="deposit" min="0" step="500"
                 value="<?= old('deposit') ?>">
        </div>

        <div class="field">
          <label for="area_sqft">Built-up area (sq.ft)</label>
          <input type="number" id="area_sqft" name="area_sqft" min="1" value="<?= old('area_sqft') ?>" required>
        </div>

        <div class="field">
          <label for="furnishing">Furnishing</label>
          <select id="furnishing" name="furnishing">
            <?php foreach (['Unfurnished','Semi-Furnished','Fully-Furnished'] as $f): ?>
              <option value="<?= $f ?>"><?= $f ?></option>
            <?php endforeach; ?>
          </select>
        </div>

        <div class="field">
          <label for="available_from">Available from</label>
          <input type="date" id="available_from" name="available_from"
                 value="<?= old('available_from', date('Y-m-d')) ?>">
        </div>

        <div class="field">
          <label for="cover">Cover image (JPG / PNG / WEBP, max 2 MB)</label>
          <input type="file" id="cover" name="cover" accept="image/jpeg,image/png,image/webp">
        </div>

        <div class="field full">
          <label for="description">Description</label>
          <textarea id="description" name="description" rows="5"
                    placeholder="Describe the property, nearby landmarks and amenities…"><?= old('description') ?></textarea>
        </div>
      </div>

      <button class="btn" type="submit" style="margin-top:1rem">Publish listing</button>
      <a class="btn btn-ghost" href="owner_dashboard.php">Cancel</a>
    </form>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
