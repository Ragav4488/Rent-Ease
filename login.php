<?php
/** RentEase – login.php : authenticate against the users table */
require_once __DIR__ . '/includes/functions.php';

if (is_logged_in()) {
    redirect(is_owner() ? 'owner_dashboard.php' : 'tenant_dashboard.php');
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $email = trim($_POST['email'] ?? '');
    $pass  = $_POST['password'] ?? '';

    $stmt = db()->prepare('SELECT * FROM users WHERE email = ? LIMIT 1');
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if ($user && password_verify($pass, $user['password_hash'])) {
        session_regenerate_id(true);
        $_SESSION['user'] = [
            'user_id'   => (int) $user['user_id'],
            'full_name' => $user['full_name'],
            'email'     => $user['email'],
            'role'      => $user['role'],
        ];
        flash('Logged in as ' . $user['full_name'] . '.');
        redirect($user['role'] === 'owner' ? 'owner_dashboard.php' : 'tenant_dashboard.php');
    }

    $error = 'Invalid email or password. Please try again.';
}

$pageTitle = 'Log in';
require __DIR__ . '/includes/header.php';
?>

<div class="wrap">
  <form class="auth" method="post" action="login.php" data-validate>
    <?= csrf_field() ?>
    <h1>Welcome back</h1>
    <p class="muted">Sign in to manage your properties, applications and payments.</p>

    <?php if ($error): ?>
      <div class="flash flash-error" style="margin-bottom:1rem"><?= e($error) ?></div>
    <?php endif; ?>

    <div class="field" style="margin-bottom:.9rem">
      <label for="email">Email address</label>
      <input type="email" id="email" name="email" value="<?= old('email') ?>" required>
      <div class="hint" data-error-for="email" style="color:var(--red);display:none"></div>
    </div>

    <div class="field" style="margin-bottom:1.2rem">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required>
      <div class="hint" data-error-for="password" style="color:var(--red);display:none"></div>
    </div>

    <button class="btn btn-block" type="submit">Log in</button>

    <div class="panel" style="margin:1.2rem 0 0;box-shadow:none;background:var(--brand-tint);border-color:#c8e6e2">
      <strong style="font-size:.85rem">Demo accounts</strong>
      <p class="muted" style="margin:.4rem 0 0">
        Owner: <code>ragav.owner@rentease.in</code><br>
        Tenant: <code>arjun.tenant@rentease.in</code><br>
        Password for both: <code>rent@1234</code>
      </p>
    </div>

    <p class="muted" style="text-align:center;margin:1rem 0 0">
      New here? <a href="register.php">Create an account</a>
    </p>
  </form>
</div>

<?php require __DIR__ . '/includes/footer.php'; ?>
