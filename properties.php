<?php
/**
 * RentEase – properties.php
 * Property listing with search + multi-facet filters, sorting and pagination.
 * Filters are built dynamically and every value is bound through PDO.
 */
require_once __DIR__ . '/includes/functions.php';

const PER_PAGE = 6;

$q         = trim($_GET['q'] ?? '');
$city      = trim($_GET['city'] ?? '');
$bhk       = trim($_GET['bhk'] ?? '');
$type      = trim($_GET['type'] ?? '');
$maxRent   = trim($_GET['max_rent'] ?? '');
$furnish   = trim($_GET['furnishing'] ?? '');
$sort      = $_GET['sort'] ?? 'newest';
$page      = max(1, (int) ($_GET['page'] ?? 1));

$where  = ['p.status <> "inactive"'];
$params = [];

if ($q !== '') {
    $where[]  = '(p.title LIKE ? OR p.locality LIKE ? OR p.city LIKE ? OR p.address LIKE ?)';
    $like     = '%' . $q . '%';
    array_push($params, $like, $like, $like, $like);
}
if ($city !== '') {
    $where[]  = 'p.city = ?';
    $params[] = $city;
}
if ($bhk !== '') {
    $where[]  = 'p.bhk = ?';
    $params[] = (int) $bhk;
}
if ($type !== '') {
    $where[]  = 'p.property_type = ?';
    $params[] = $type;
}
if ($maxRent !== '') {
    $where[]  = 'p.rent_amount <= ?';
    $params[] = (float) $maxRent;
}
if ($furnish !== '') {
    $where[]  = 'p.furnishing = ?';
    $params[] = $furnish;
}

$orderBy = match ($sort) {
    'rent_asc'  => 'p.rent_amount ASC',
    'rent_desc' => 'p.rent_amount DESC',
    'area_desc' => 'p.area_sqft DESC',
    default     => 'p.created_at DESC',
};

$sqlWhere = 'WHERE ' . implode(' AND ', $where);

/* total rows for pagination */
$cnt = db()->prepare("SELECT COUNT(*) FROM properties p $sqlWhere");
$cnt->execute($params);
$total = (int) $cnt->fetchColumn();

$pages = max(1, (int) ceil($total / PER_PAGE));
$page  = min($page, $pages);
$offset = ($page - 1) * PER_PAGE;

$stmt = db()->prepare(
    "SELECT p.*, u.full_name AS owner_name
       FROM properties p
       JOIN users u ON u.user_id = p.owner_id
      $sqlWhere
      ORDER BY $orderBy
      LIMIT " . PER_PAGE . " OFFSET $offset"
);
$stmt->execute($params);
$rows = $stmt->fetchAll();

$cities = db()->query('SELECT DISTINCT city FROM properties ORDER BY city')->fetchAll(PDO::FETCH_COLUMN);
$types  = db()->query('SELECT DISTINCT property_type FROM properties ORDER BY property_type')->fetchAll(PDO::FETCH_COLUMN);

$pageTitle = 'Browse properties';
require __DIR__ . '/includes/header.php';
?>

<section class="section" style="padding-top:1.8rem">
  <div class="wrap">

    <div class="section-head">
      <div>
        <h1 style="margin-bottom:.2rem">Browse properties</h1>
        <p class="muted" style="margin:0">
          <strong id="filterCount"><?= $total ?></strong> propert<?= $total === 1 ? 'y' : 'ies' ?>
          match<?= $total === 1 ? 'es' : '' ?> your filters
        </p>
      </div>
    </div>

    <form class="panel" method="get" action="properties.php" style="margin-bottom:1.4rem">
      <div class="form-grid" style="grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.8rem">
        <div class="field">
          <label for="q">Keyword</label>
          <input type="search" id="q" name="q" value="<?= e($q) ?>" placeholder="Locality or title">
        </div>
        <div class="field">
          <label for="city">City</label>
          <select id="city" name="city">
            <option value="">All cities</option>
            <?php foreach ($cities as $c): ?>
              <option value="<?= e($c) ?>" <?= $city === $c ? 'selected' : '' ?>><?= e($c) ?></option>
            <?php endforeach; ?>
          </select>
        </div>
        <div class="field">
          <label for="bhk">Bedrooms</label>
          <select id="bhk" name="bhk">
            <option value="">Any</option>
            <?php foreach ([1, 2, 3] as $b): ?>
              <option value="<?= $b ?>" <?= $bhk === (string) $b ? 'selected' : '' ?>><?= $b ?> BHK</option>
            <?php endforeach; ?>
          </select>
        </div>
        <div class="field">
          <label for="type">Property type</label>
          <select id="type" name="type">
            <option value="">Any type</option>
            <?php foreach ($types as $t): ?>
              <option value="<?= e($t) ?>" <?= $type === $t ? 'selected' : '' ?>><?= e($t) ?></option>
            <?php endforeach; ?>
          </select>
        </div>
        <div class="field">
          <label for="furnishing">Furnishing</label>
          <select id="furnishing" name="furnishing">
            <option value="">Any</option>
            <?php foreach (['Unfurnished','Semi-Furnished','Fully-Furnished'] as $f): ?>
              <option value="<?= e($f) ?>" <?= $furnish === $f ? 'selected' : '' ?>><?= e($f) ?></option>
            <?php endforeach; ?>
          </select>
        </div>
        <div class="field">
          <label for="max_rent">Max rent (₹)</label>
          <input type="number" id="max_rent" name="max_rent" min="0" step="500"
                 value="<?= e($maxRent) ?>" placeholder="e.g. 25000">
        </div>
        <div class="field">
          <label for="sort">Sort by</label>
          <select id="sort" name="sort">
            <option value="newest"     <?= $sort === 'newest'    ? 'selected' : '' ?>>Newest first</option>
            <option value="rent_asc"   <?= $sort === 'rent_asc'  ? 'selected' : '' ?>>Rent: low to high</option>
            <option value="rent_desc"  <?= $sort === 'rent_desc' ? 'selected' : '' ?>>Rent: high to low</option>
            <option value="area_desc"  <?= $sort === 'area_desc' ? 'selected' : '' ?>>Largest area</option>
          </select>
        </div>
        <div class="field" style="display:flex;gap:.5rem;align-items:flex-end">
          <button class="btn" type="submit">Apply filters</button>
          <a class="btn btn-ghost" href="properties.php">Reset</a>
        </div>
      </div>
      <p class="hint" style="margin:.7rem 0 0">
        Tip: type in the keyword box and every card filters live as you type.
      </p>
      <input type="search" id="liveFilter" placeholder="Live filter results on this page…"
             style="margin-top:.5rem">
    </form>

    <?php if (!$rows): ?>
      <div class="panel empty">
        <strong>No properties matched</strong>
        Try widening the budget, clearing the city filter or searching a different locality.
      </div>
    <?php else: ?>
      <div class="cards">
        <?php foreach ($rows as $p): ?>
          <article class="prop-card"
                   data-search="<?= e($p['title'] . ' ' . $p['locality'] . ' ' . $p['city'] . ' ' . $p['property_type']) ?>">
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
                <span><?= e($p['furnishing']) ?></span>
              </div>
              <div class="prop-meta">
                <span>📍 <?= e($p['locality']) ?>, <?= e($p['city']) ?></span>
              </div>
              <div class="prop-foot">
                <span class="<?= status_class($p['status']) ?>"><?= e($p['status']) ?></span>
                <a class="btn btn-ghost btn-sm" href="property.php?id=<?= (int) $p['property_id'] ?>">Details</a>
              </div>
            </div>
          </article>
        <?php endforeach; ?>
      </div>

      <?php if ($pages > 1): ?>
        <nav class="pager">
          <?php
          $qs = $_GET;
          for ($i = 1; $i <= $pages; $i++):
              $qs['page'] = $i;
          ?>
            <?php if ($i === $page): ?>
              <span class="on"><?= $i ?></span>
            <?php else: ?>
              <a href="properties.php?<?= e(http_build_query($qs)) ?>"><?= $i ?></a>
            <?php endif; ?>
          <?php endfor; ?>
        </nav>
      <?php endif; ?>
    <?php endif; ?>

  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
