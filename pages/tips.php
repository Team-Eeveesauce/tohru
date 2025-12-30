<?php
// tips.php - Browse tips
require_once 'config.php';

$pdo = getDB();
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$search = isset($_GET['search']) ? trim($_GET['search']) : '';

$where = "WHERE visible = 1";
$params = [];

if ($search) {
    $where .= " AND (content LIKE ? OR author LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

$countStmt = $pdo->prepare("SELECT COUNT(*) FROM tips $where");
$countStmt->execute($params);
$total = $countStmt->fetchColumn();

$pagination = getPagination($total, $page, ITEMS_PER_PAGE);

$stmt = $pdo->prepare("
    SELECT id, content, author, submitter_id, submission_time 
    FROM tips 
    $where 
    ORDER BY submission_time DESC 
    LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
");
$stmt->execute($params);
$tips = $stmt->fetchAll();
?>
    <title>Tips - Tohru Database</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>💡 Tips</h1>
            <a href="index.php" class="back-link">← Back to Home</a>
        </header>

        <div class="search-bar">
            <form method="GET" action="">
                <input type="text" name="search" placeholder="Search tips or authors..." value="<?= e($search) ?>">
                <button type="submit">Search</button>
                <?php if ($search): ?>
                    <a href="tips.php" class="clear-search">Clear</a>
                <?php endif; ?>
            </form>
        </div>

        <div class="results-info">
            Showing <?= $pagination['offset'] + 1 ?> - <?= min($pagination['offset'] + $pagination['perPage'], $total) ?> of <?= $total ?> tips
        </div>

        <div class="items-list">
            <?php foreach ($tips as $tip): ?>
                <div class="item-card tip-card">
                    <div class="tip-content">
                        <p><?= e($tip['content']) ?></p>
                    </div>
                    <div class="tip-meta">
                        <span class="author">— <?= e($tip['author']) ?></span>
                        <span class="meta-info">
                            ID: <?= $tip['id'] ?> | 
                            Submitted: <?= date('Y-m-d H:i', strtotime($tip['submission_time'])) ?>
                            <?php if ($tip['submitter_id']): ?>
                                | By: <?= $tip['submitter_id'] ?>
                            <?php endif; ?>
                        </span>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php if (empty($tips)): ?>
                <p class="no-results">No tips found.</p>
            <?php endif; ?>
        </div>

        <?php if ($pagination['totalPages'] > 1): ?>
            <div class="pagination">
                <?php if ($page > 1): ?>
                    <a href="?page=1<?= $search ? '&search=' . urlencode($search) : '' ?>">&laquo; First</a>
                    <a href="?page=<?= $page - 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Previous</a>
                <?php endif; ?>

                <span class="page-info">Page <?= $page ?> of <?= $pagination['totalPages'] ?></span>

                <?php if ($page < $pagination['totalPages']): ?>
                    <a href="?page=<?= $page + 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Next</a>
                    <a href="?page=<?= $pagination['totalPages'] ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Last &raquo;</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>