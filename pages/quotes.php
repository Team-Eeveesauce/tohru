<?php
$pdo = getDB();
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$search = isset($_GET['search']) ? trim($_GET['search']) : '';

// Build query
$where = "WHERE visible = 1";
$params = [];

if ($search) {
    $where .= " AND (content LIKE ? OR author LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

// Get total count
$countStmt = $pdo->prepare("SELECT COUNT(*) FROM quotes $where");
$countStmt->execute($params);
$total = $countStmt->fetchColumn();

// Get pagination info
$pagination = getPagination($total, $page, ITEMS_PER_PAGE);

// Get quotes
$stmt = $pdo->prepare("
    SELECT id, content, author, submitter_id, submission_time 
    FROM quotes 
    $where 
    ORDER BY submission_time DESC 
    LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
");
$stmt->execute($params);
$quotes = $stmt->fetchAll();
?>
    <title>Quotes - Tohru Database</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>💬 Quotes</h1>
            <a href="<?php echo $basePath; ?>" class="back-link">← Back to Home</a>
        </header>

        <div class="search-bar">
            <form method="GET" action="">
                <input type="hidden" name="i" value="quotes">
                <input type="text" name="search" placeholder="Search quotes or authors..." value="<?= e($search) ?>">
                <button type="submit">Search</button>
                <?php if ($search): ?>
                    <a href="?i=quotes" class="clear-search">Clear</a>
                <?php endif; ?>
            </form>
        </div>

        <div class="results-info">
            Showing <?= $pagination['offset'] + 1 ?> - <?= min($pagination['offset'] + $pagination['perPage'], $total) ?> of <?= $total ?> quotes
        </div>

        <div class="items-list">
            <?php foreach ($quotes as $quote): ?>
                <div class="item-card quote-card">
                    <div class="quote-content">
                        <p>"<?= e($quote['content']) ?>"</p>
                    </div>
                    <div class="quote-meta">
                        <span class="author">— <?= e($quote['author']) ?></span>
                        <span class="meta-info">
                            ID: <?= $quote['id'] ?> | 
                            Submitted: <?= date('Y-m-d H:i', strtotime($quote['submission_time'])) ?>
                            <?php if ($quote['submitter_id']): ?>
                                | By: <?= $quote['submitter_id'] ?>
                            <?php endif; ?>
                        </span>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php if (empty($quotes)): ?>
                <p class="no-results">No quotes found.</p>
            <?php endif; ?>
        </div>

        <?php if ($pagination['totalPages'] > 1): ?>
            <div class="pagination">
                <?php if ($page > 1): ?>
                    <a href="?i=quotes&page=1<?= $search ? '&search=' . urlencode($search) : '' ?>">&laquo; First</a>
                    <a href="?i=quotes&page=<?= $page - 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Previous</a>
                <?php endif; ?>

                <span class="page-info">Page <?= $page ?> of <?= $pagination['totalPages'] ?></span>

                <?php if ($page < $pagination['totalPages']): ?>
                    <a href="?i=quotes&page=<?= $page + 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Next</a>
                    <a href="?i=quotes&page=<?= $pagination['totalPages'] ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Last &raquo;</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>