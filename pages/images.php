<?php
$pdo = getDB();
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$search = isset($_GET['search']) ? trim($_GET['search']) : '';

$where = "WHERE 1=1";
$params = [];

if ($search) {
    $where .= " AND caption LIKE ?";
    $params[] = "%$search%";
}

$countStmt = $pdo->prepare("SELECT COUNT(*) FROM archives_image $where");
$countStmt->execute($params);
$total = $countStmt->fetchColumn();

$pagination = getPagination($total, $page, ITEMS_PER_PAGE);

$stmt = $pdo->prepare("
    SELECT id, path, original_path, caption, colour, submitter_id, submission_time 
    FROM archives_image 
    $where 
    ORDER BY submission_time DESC 
    LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
");
$stmt->execute($params);
$images = $stmt->fetchAll();
?>
    <title>Images - Tohru Database</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>🖼️ Image Archives</h1>
            <a href="." class="back-link">← Back to Home</a>
        </header>

        <div class="search-bar">
            <form method="GET" action="">
                <input type="hidden" name="i" value="images">
                <input type="text" name="search" placeholder="Search captions..." value="<?= e($search) ?>">
                <button type="submit">Search</button>
                <?php if ($search): ?>
                    <a href="?i=images" class="clear-search">Clear</a>
                <?php endif; ?>
            </form>
        </div>

        <div class="results-info">
            Showing <?= $pagination['offset'] + 1 ?> - <?= min($pagination['offset'] + $pagination['perPage'], $total) ?> of <?= $total ?> images
        </div>

        <div class="gallery">
            <?php foreach ($images as $img): ?>
                <div class="gallery-item" style="border-color: <?= e($img['colour']) ?>">
                    <div class="gallery-image">
                        <img src="<?= e($img['path']) ?>" alt="<?= e($img['caption']) ?>" loading="lazy">
                    </div>
                    <div class="gallery-caption">
                        <p><?= e($img['caption']) ?></p>
                        <div class="meta-info">
                            ID: <?= $img['id'] ?> | 
                            <?= date('Y-m-d', strtotime($img['submission_time'])) ?>
                            <?php if ($img['submitter_id']): ?>
                                | By: <?= $img['submitter_id'] ?>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php if (empty($images)): ?>
                <p class="no-results">No images found.</p>
            <?php endif; ?>
        </div>

        <?php if ($pagination['totalPages'] > 1): ?>
            <div class="pagination">
                <?php if ($page > 1): ?>
                    <a href="?i=images&page=1<?= $search ? '&search=' . urlencode($search) : '' ?>">&laquo; First</a>
                    <a href="?i=images&page=<?= $page - 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Previous</a>
                <?php endif; ?>

                <span class="page-info">Page <?= $page ?> of <?= $pagination['totalPages'] ?></span>

                <?php if ($page < $pagination['totalPages']): ?>
                    <a href="?i=images&page=<?= $page + 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Next</a>
                    <a href="?i=images&page=<?= $pagination['totalPages'] ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Last &raquo;</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>