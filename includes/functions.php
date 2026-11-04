<?php
/**
 * RentEase – includes/functions.php
 * Session bootstrap, authentication guards, CSRF token and small helpers
 * shared by every page.
 */

declare(strict_types=1);

require_once __DIR__ . '/../config/db.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

/* ---------------------------------------------------------------
 |  Authentication helpers
 * --------------------------------------------------------------- */

function current_user(): ?array
{
    return $_SESSION['user'] ?? null;
}

function is_logged_in(): bool
{
    return isset($_SESSION['user']);
}

function is_owner(): bool
{
    return (current_user()['role'] ?? '') === 'owner';
}

function is_tenant(): bool
{
    return (current_user()['role'] ?? '') === 'tenant';
}

function require_login(): void
{
    if (!is_logged_in()) {
        header('Location: login.php?next=' . urlencode($_SERVER['REQUEST_URI'] ?? 'index.php'));
        exit;
    }
}

function require_role(string $role): void
{
    require_login();
    if ((current_user()['role'] ?? '') !== $role) {
        http_response_code(403);
        exit('<p style="font-family:Arial">403 – this page is for '
            . htmlspecialchars($role) . ' accounts only.</p>');
    }
}

/* ---------------------------------------------------------------
 |  CSRF protection
 * --------------------------------------------------------------- */

function csrf_token(): string
{
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(16));
    }
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="csrf" value="' . csrf_token() . '">';
}

function verify_csrf(): void
{
    $sent = $_POST['csrf'] ?? '';
    if (!is_string($sent) || !hash_equals($_SESSION['csrf'] ?? '', $sent)) {
        http_response_code(419);
        exit('<p style="font-family:Arial">Session expired. Please reload the page.</p>');
    }
}

/* ---------------------------------------------------------------
 |  Output helpers
 * --------------------------------------------------------------- */

function e(?string $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}

function money(float|string $amount): string
{
    return '₹' . number_format((float) $amount, 0, '.', ',');
}

function flash(?string $message = null, string $type = 'success'): ?array
{
    if ($message !== null) {
        $_SESSION['flash'] = ['msg' => $message, 'type' => $type];
        return null;
    }
    $f = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $f;
}

function redirect(string $to): never
{
    header('Location: ' . $to);
    exit;
}

function old(string $key, string $default = ''): string
{
    return e($_POST[$key] ?? $default);
}

function month_label(string $date): string
{
    return date('M Y', strtotime($date));
}

function status_class(string $status): string
{
    return match ($status) {
        'available', 'approved', 'resolved' => 'chip chip-green',
        'occupied', 'in-progress'           => 'chip chip-blue',
        'pending', 'open'                   => 'chip chip-amber',
        'rejected', 'inactive'              => 'chip chip-red',
        default                             => 'chip',
    };
}
