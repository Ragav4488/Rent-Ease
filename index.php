<?php
/** RentEase – index.php : landing page with hero + featured listings */
require_once __DIR__ . '/includes/functions.php';

$cities = db()->query('SELECT DISTINCT city FROM properties ORDER BY city')
              ->fetchAll(PDO::FETCH_COLUMN);

$featured = db()->query(
    'SELECT p.*, u.full_name AS owner_name
       FROM properties p
       JOIN users u ON u.user_id = p.owner_id
      WHERE p.status = "available"
      ORDER BY p.created_at DESC
      LIMIT 6'
)->fetchAll();

$counts = db()->query(
    'SELECT
        (SELECT COUNT(*) FROM properties WHERE status="available") AS available,
        (SELECT COUNT(*) FROM properties)                          AS total,
        (SELECT COUNT(DISTINCT city) FROM properties)              AS cities,
        (SELECT COUNT(*) FROM users WHERE role="tenant")           AS tenants'
)->fetch();

$pageTitle = 'Find your next home';
require __DIR__ . '/includes/header.php';
?>

<section class="hero">
  <div class="wrap">
    <h1>Rent smarter. Live better.</h1>
    <p class="lead">
      RentEase connects property owners with verified tenants — search listings,
      apply online, pay rent and track maintenance complaints in one place.
    </p>
  </div>
</section>

<div class="wrap">
  <form class="search-card" action="properties.php" method="get">
    <div class="search-grid">
      <div class="field">
        <label for="q">Where do you want to live?</label>
        <input type="search" id="q" name="q" placeholder="Locality, city or property name">
      </div>
      <div class="field">
        <label for="city">City</label>
        <select id="city" name="city">
          <option value="">Any city</option>
          <?php foreach ($cities as $c): ?>
            <option value="<?= e($c) ?>"><?= e($c) ?></option>
          <?php endforeach; ?>
        </select>
      </div>
      <div class="field">
        <label for="bhk">BHK</label>
        <select id="bhk" name="bhk">
          <option value="">Any</option>
          <option value="1">1 BHK</option>
          <option value="2">2 BHK</option>
          <option value="3">3 BHK</option>
        </select>
      </div>
      <div class="field">
        <label for="max_rent">Max rent</label>
        <select id="max_rent" name="max_rent">
          <option value="">No limit</option>
          <option value="10000">₹10,000</option>
          <option value="20000">₹20,000</option>
          <option value="35000">₹35,000</option>
          <option value="50000">₹50,000</option>
        </select>
      </div>
      <div class="field">
        <button class="btn" type="submit">Search</button>
      </div>
    </div>
  </form>
</div>

<section class="section">
  <div class="wrap">
    <div class="stats">
      <div class="stat">
        <div class="label">Available now</div>
        <div class="value"><?= (int) $counts['available'] ?></div>
        <div class="sub">of <?= (int) $counts['total'] ?> listed properties</div>
      </div>
      <div class="stat">
        <div class="label">Cities covered</div>
        <div class="value"><?= (int) $counts['cities'] ?></div>
        <div class="sub">Coimbatore &amp; Chennai</div>
      </div>
      <div class="stat">
        <div class="label">Registered tenants</div>
        <div class="value"><?= (int) $counts['tenants'] ?></div>
        <div class="sub">verified with email + mobile</div>
      </div>
      <div class="stat">
        <div class="label">Zero brokerage</div>
        <div class="value">₹0</div>
        <div class="sub">owners deal with tenants directly</div>
      </div>
    </div>

    <div class="section-head">
      <h2>Featured properties</h2>
      <a href="properties.php">View all listings →</a>
    </div>

    <div class="cards">
      <?php foreach ($featured as $p): ?>
        <article class="prop-card">
          <div class="prop-thumb">
            <img src="<?= e($p['cover_image']) ?>" alt="<?= e($p['title']) ?>">
            <span class="price-tag"><?= money($p['rent_amount']) ?>/mo</span>
          </div>
          <div class="prop-body">
            <h3><a href="property.php?id=<?= (int) $p['property_id'] ?>"><?= e($p['title']) ?></a></h3>
            <div class="prop-meta">
              <span><?= (int) $p['bhk'] ?> BHK</span>
              <span><?= e($p['property_type']) ?></span>
              <span><?= (int) $p['area_sqft'] ?> sq.ft</span>
            </div>
            <div class="prop-meta"><span>📍 <?= e($p['locality']) ?>, <?= e($p['city']) ?></span></div>
            <div class="prop-foot">
              <span class="<?= status_class($p['status']) ?>"><?= e($p['status']) ?></span>
              <a class="btn btn-ghost btn-sm"
                 href="property.php?id=<?= (int) $p['property_id'] ?>">View details</a>
            </div>
          </div>
        </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <div class="section-head"><h2>How RentEase works</h2></div>
    <div class="cards">
      <div class="panel">
        <h3>1 · Browse &amp; filter</h3>
        <p class="muted">Search by city, locality, BHK, property type and budget.
           Every listing carries a photo gallery and a full specification sheet.</p>
      </div>
      <div class="panel">
        <h3>2 · Apply online</h3>
        <p class="muted">Submit a rental application with your occupation and family size.
           The owner approves or rejects it from the dashboard.</p>
      </div>
      <div class="panel">
        <h3>3 · Pay &amp; maintain</h3>
        <p class="muted">Record monthly rent against a transaction reference and raise
           maintenance complaints that the owner tracks to resolution.</p>
      </div>
    </div>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
