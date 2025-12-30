<?php
// config.php - Database configuration
define('DB_HOST', '127.0.0.1');
define('DB_NAME', 'tohru');
define('DB_USER', 'root');
define('DB_PASS', '');

function getDB() {
    try {
        $pdo = new PDO(
            "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4",
            DB_USER,
            DB_PASS,
            [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            ]
        );
        return $pdo;
    } catch (PDOException $e) {
        die("Database connection failed: " . $e->getMessage());
    }
}

// Pagination settings
define('ITEMS_PER_PAGE', 20);

// Helper function for pagination
function getPagination($total, $page, $perPage) {
    $totalPages = ceil($total / $perPage);
    $page = max(1, min($page, $totalPages));
    $offset = ($page - 1) * $perPage;
    
    return [
        'total' => $total,
        'totalPages' => $totalPages,
        'currentPage' => $page,
        'offset' => $offset,
        'perPage' => $perPage
    ];
}

// Helper function to escape output
function e($string) {
    return htmlspecialchars($string ?? '', ENT_QUOTES, 'UTF-8');
}
?>