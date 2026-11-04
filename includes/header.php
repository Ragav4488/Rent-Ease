<?php
/**
 * RentEase – includes/header.php
 * Shared top navigation. Pages set $pageTitle before including this file.
 */
$pageTitle = $pageTitle ?? 'RentEase';
$flashes   = flash();
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($pageTitle) ?> · RentEase</title>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

<header class="site-header">
  <div class="wrap header-inner">

    <a class="brand" href="index.php">
      <span class="brand-mark">RE</span>
      <span class="brand-text">Rent<em>Ease</em></span>
    </a>

    <input type="checkbox" id="navToggle" class="nav-toggle">
    <label for="navToggle" class="nav-burger" aria-label="Toggle navigation">
      <span></span><span></span><span></span>
    </label>

    <nav class="site-nav">
      <a href="index.php">Home</a>
      <a href="properties.php">Properties</a>

      <?php if (is_tenant()): ?>
        <a href="tenant_dashboard.php">My Dashboard</a>
      <?php elseif (is_owner()): ?>
        <a href="owner_dashboard.php">Owner Dashboard</a>
      <?php endif; ?>

      <?php if (is_logged_in()): ?>
        <span class="nav-user">
          <span class="avatar"><?= e(strtoupper(substr(current_user()['full_name'], 0, 1))) ?></span>
          <?= e(current_user()['full_name']) ?>
        </span>
        <a class="btn btn-ghost btn-sm" href="logout.php">Logout</a>
      <?php else: ?>
        <a href="login.php">Login</a>
        <a class="btn btn-primary btn-sm" href="register.php">Register</a>
      <?php endif; ?>
    </nav>

  </div>
</header>

<?php if ($flashes): ?>
  <div class="wrap">
    <div class="flash flash-<?= e($flashes['type']) ?>"><?= e($flashes['msg']) ?></div>
  </div>
<?php endif; ?>

<main>
