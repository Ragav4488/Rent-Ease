<?php
/**
 * RentEase – config/db.php
 *
 * One PDO handle for the whole application.
 *
 * Resolution order:
 *   1. MySQL, when the server is reachable and the database exists.
 *   2. SQLite, created and seeded automatically at database/rentease.sqlite.
 *
 * The fallback exists so the application runs on a host with no MySQL
 * service and no database setup — including free tiers and fresh clones of
 * this repository — without a single line of configuration.
 */

declare(strict_types=1);

const DB_HOST = '127.0.0.1';
const DB_PORT = 3306;            // 3307 on the author's machine
const DB_NAME = 'rentease';
const DB_USER = 'root';
const DB_PASS = '';

/** Set to false to skip MySQL entirely and always use SQLite. */
const USE_MYSQL = true;

const SQLITE_PATH = __DIR__ . '/../database/rentease.sqlite';

function db(): PDO
{
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    if (USE_MYSQL) {
        try {
            $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
                DB_HOST, DB_PORT, DB_NAME);
            $pdo = new PDO($dsn, DB_USER, DB_PASS, [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
            ]);
            return $pdo;
        } catch (PDOException $e) {
            // fall through to SQLite
        }
    }

    $pdo = sqlite_connect();
    return $pdo;
}

function sqlite_connect(): PDO
{
    $dir = dirname(SQLITE_PATH);
    if (!is_dir($dir)) {
        mkdir($dir, 0775, true);
    }

    $fresh = !file_exists(SQLITE_PATH) || filesize(SQLITE_PATH) === 0;

    $pdo = new PDO('sqlite:' . SQLITE_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA foreign_keys = ON');

    if ($fresh) {
        sqlite_seed($pdo);
    }

    return $pdo;
}

/** Create the six tables and the demonstration data in one transaction. */
function sqlite_seed(PDO $pdo): void
{
    $path = __DIR__ . '/../database/seed_sqlite.sql';
    if (!file_exists($path)) {
        throw new RuntimeException('SQLite seed file missing: database/seed_sqlite.sql');
    }

    $pdo->beginTransaction();
    try {
        foreach (split_sql(file_get_contents($path)) as $stmt) {
            $pdo->exec($stmt);
        }
        $pdo->commit();
    } catch (Throwable $e) {
        $pdo->rollBack();
        throw $e;
    }
}

/** Split a script on semicolons that are not inside a quoted string. */
function split_sql(string $sql): array
{
    $out = [];
    $buf = '';
    $quote = null;

    foreach (str_split($sql) as $ch) {
        if ($quote !== null) {
            $buf .= $ch;
            if ($ch === $quote) {
                $quote = null;
            }
            continue;
        }
        if ($ch === "'" || $ch === '"') {
            $quote = $ch;
            $buf .= $ch;
            continue;
        }
        if ($ch === ';') {
            if (trim($buf) !== '') {
                $out[] = trim($buf);
            }
            $buf = '';
            continue;
        }
        $buf .= $ch;
    }
    if (trim($buf) !== '') {
        $out[] = trim($buf);
    }
    return $out;
}
