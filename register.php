<?php
/** RentEase – register.php : create an owner or tenant account */
require_once __DIR__ . '/includes/functions.php';

if (is_logged_in()) {
    redirect(is_owner() ? 'owner_dashboard.php' : 'tenant_dashboard.php');
}

$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    verify_csrf();

    $name    = trim($_POST['full_name'] ?? '');
    $email   = trim($_POST['email'] ?? '');
    $phone   = trim($_POST['phone'] ?? '');
    $role    = ($_POST['role'] ?? 'tenant') === 'owner' ? 'owner' : 'tenant';
    $pass    = $_POST['password'] ?? '';
    $confirm = $_POST['confirm'] ?? '';

    if (mb_strlen($name) < 3) {
        $errors['full_name'] = 'Enter your full name (minimum 3 characters).';
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Enter a valid email address.';
    }
    if (!preg_match('/^[6-9]\d{9}$/', $phone)) {
        $errors['phone'] = 'Enter a valid 10-digit Indian mobile number.';
    }
    if (strlen($pass) < 8) {
        $errors['password'] = 'Password must be at least 8 characters.';
    } elseif ($pass !== $confirm) {
        $errors['confirm'] = 'Passwords do not match.';
    }

    if (!$errors) {
        $stmt = db()->prepare('SELECT user_id FROM users WHERE email = ?');
        $stmt->execute([$email]);
        if ($stmt->fetch()) {
            $errors['email'] = 'This email is already registered. Try logging in.';
        }
    }

    if (!$errors) {
        $stmt = db()->prepare(
            'INSERT INTO users (full_name, email, phone, password_hash, role)
             VALUES (?, ?, ?, ?, ?)'
        );
        $stmt->execute([$name, $email, $phone,
                        password_hash($pass, PASSWORD_DEFAULT), $role]);

        $_SESSION['user'] = [
            'user_id'   => (int) db()->lastInsertId(),
            'full_name' => $name,
            'email'     => $email,
            'role'      => $role,
        ];
        flash('Welcome to RentEase, ' . $name . '!');
        redirect($role === 'owner' ? 'owner_dashboard.php' : 'tenant_dashboard.php');
    }
}

$pageTitle = 'Create an account';
require __DIR__ . '/includes/header.php';
?>

<div class="wrap">
  <form class="auth" method="post" action="register.php" data-validate>
    <?= csrf_field() ?>
    <h1>Create your account</h1>
    <p class="muted">Owners list properties; tenants apply, pay rent and raise complaints.</p>

    <div class="role-pick">
      <label>
        <input type="radio" name="role" value="tenant" checked>
        <span>🔑 I am a Tenant</span>
      </label>
      <label>
        <input type="radio" name="role" value="owner">
        <span>🏠 I am an Owner</span>
      </label>
    </div>

    <div class="field" style="margin-bottom:.9rem">
      <label for="full_name">Full name</label>
      <input type="text" id="full_name" name="full_name" value="<?= old('full_name') ?>" required>
      <div class="hint" data-error-for="full_name" style="color:var(--red);display:none"><?= e($errors['full_name'] ?? '') ?></div>
    </div>

    <div class="field" style="margin-bottom:.9rem">
      <label for="email">Email address</label>
      <input type="email" id="email" name="email" value="<?= old('email') ?>" required>
      <div class="hint" data-error-for="email" style="color:var(--red);display:none"><?= e($errors['email'] ?? '') ?></div>
    </div>

    <div class="field" style="margin-bottom:.9rem">
      <label for="phone">Mobile number</label>
      <input type="tel" id="phone" name="phone" maxlength="10" value="<?= old('phone') ?>" required>
      <div class="hint" data-error-for="phone" style="color:var(--red);display:none"><?= e($errors['phone'] ?? '') ?></div>
    </div>

    <div class="form-grid">
      <div class="field">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
        <div class="hint" data-error-for="password" style="color:var(--red);display:none"><?= e($errors['password'] ?? '') ?></div>
      </div>
      <div class="field">
        <label for="confirm">Confirm password</label>
        <input type="password" id="confirm" name="confirm" required>
        <div class="hint" data-error-for="confirm" style="color:var(--red);display:none"><?= e($errors['confirm'] ?? '') ?></div>
      </div>
    </div>

    <button class="btn btn-block" type="submit" style="margin-top:1.2rem">Create account</button>
    <p class="muted" style="text-align:center;margin:.9rem 0 0">
      Already registered? <a href="login.php">Log in</a>
    </p>
  </form>
</div>

<?php require __DIR__ . '/includes/footer.php'; ?>
