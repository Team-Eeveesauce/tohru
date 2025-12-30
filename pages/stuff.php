<?php
// stuff.php - Browse stuff
require_once 'config.php';

$pdo = getDB();
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$search = isset($_GET['search']) ? trim($_GET['search']) : '';
$type = isset($_GET['type']) ? trim($_GET['type']) : '';

$where = "WHERE visible = 1";
$params = [];

if ($search) {
    $where .= " AND (name LIKE ? OR description LIKE ? OR fact LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

if ($type) {
    $where .= " AND type = ?";
    $params[] = $type;
}

// Get types for filter
$typesStmt = $pdo->query("SELECT DISTINCT type FROM stuff WHERE visible = 1 ORDER BY type");
$types = $typesStmt->fetchAll(PDO::FETCH_COLUMN);

$countStmt = $pdo->prepare("SELECT COUNT(*) FROM stuff $where");
$countStmt->execute($params);
$total = $countStmt->fetchColumn();

$pagination = getPagination($total, $page, ITEMS_PER_PAGE);

$stmt = $pdo->prepare("
    SELECT id, type, name, description, fact, image, colour, submitter_id, submission_time 
    FROM stuff 
    $where 
    ORDER BY submission_time DESC 
    LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
");
$stmt->execute($params);
$items = $stmt->fetchAll();
?>
    <title>Stuff - Tohru Database</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>📦 Stuff</h1>
            <a href="index.php" class="back-link">← Back to Home</a>
        </header>

        <div class="search-bar">
            <form method="GET" action="">
                <input type="text" name="search" placeholder="Search stuff..." value="<?= e($search) ?>">
                <select name="type">
                    <option value="">All Types</option>
                    <?php foreach ($types as $t): ?>
                        <option value="<?= e($t) ?>" <?= $type === $t ? 'selected' : '' ?>><?= e($t) ?></option>
                    <?php endforeach; ?>
                </select>
                <button type="submit">Search</button>
                <?php if ($search || $type): ?>
                    <a href="stuff.php" class="clear-search">Clear</a>
                <?php endif; ?>
            </form>
        </div>

        <div class="results-info">
            Showing <?= $pagination['offset'] + 1 ?> - <?= min($pagination['offset'] + $pagination['perPage'], $total) ?> of <?= $total ?> items
        </div>

        <div class="items-list">
            <?php foreach ($items as $item): ?>
                <div class="item-card stuff-card" style="border-left: 4px solid <?= e($item['colour']) ?>">
                    <?php if ($item['image']): ?>
                        <div class="stuff-image">
                            <img src="uploads/<?= e($item['image']) ?>" alt="<?= e($item['name']) ?>" loading="lazy">
                        </div>
                    <?php endif; ?>
                    <div class="stuff-content">
                        <div class="stuff-header">
                            <h3><?= e($item['name']) ?></h3>
                            <span class="type-badge" style="background-color: <?= e($item['colour']) ?>20; color: <?= e($item['colour']) ?>">
                                <?= e($item['type']) ?>
                            </span>
                        </div>
                        <p class="description"><?= e($item['description']) ?></p>
                        <?php if ($item['fact']): ?>
                            <p class="fact"><strong>Fact:</strong> <?= e($item['fact']) ?></p>
                        <?php endif; ?>
                        <div class="meta-info">
                            ID: <?= $item['id'] ?> | 
                            Submitted: <?= date('Y-m-d H:i', strtotime($item['submission_time'])) ?>
                            | By: <?= $item['submitter_id'] ?>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php if (empty($items)): ?>
                <p class="no-results">No items found.</p>
            <?php endif; ?>
        </div>

        <?php if ($pagination['totalPages'] > 1): ?>
            <div class="pagination">
                <?php 
                $queryParams = [];
                if ($search) $queryParams[] = 'search=' . urlencode($search);
                if ($type) $queryParams[] = 'type=' . urlencode($type);
                $queryString = $queryParams ? '&' . implode('&', $queryParams) : '';
                ?>
                
                <?php if ($page > 1): ?>
                    <a href="?page=1<?= $queryString ?>">&laquo; First</a>
                    <a href="?page=<?= $page - 1 ?><?= $queryString ?>">Previous</a>
                <?php endif; ?>

                <span class="page-info">Page <?= $page ?> of <?= $pagination['totalPages'] ?></span>

                <?php if ($page < $pagination['totalPages']): ?>
                    <a href="?page=<?= $page + 1 ?><?= $queryString ?>">Next</a>
                    <a href="?page=<?= $pagination['totalPages'] ?><?= $queryString ?>">Last &raquo;</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>