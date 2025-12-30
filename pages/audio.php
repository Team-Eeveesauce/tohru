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

$countStmt = $pdo->prepare("SELECT COUNT(*) FROM archives_audio $where");
$countStmt->execute($params);
$total = $countStmt->fetchColumn();

$pagination = getPagination($total, $page, ITEMS_PER_PAGE);

$stmt = $pdo->prepare("
    SELECT id, path, original_path, caption, colour, submitter_id, submission_time 
    FROM archives_audio 
    $where 
    ORDER BY submission_time DESC 
    LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
");
$stmt->execute($params);
$audios = $stmt->fetchAll();
?>
    <title>Audio - Tohru Database</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔊 Audio Archives</h1>
            <a href="." class="back-link">← Back to Home</a>
        </header>

        <div class="search-bar">
            <form method="GET" action="">
                <input type="hidden" name="i" value="audio">
                <input type="text" name="search" placeholder="Search captions..." value="<?= e($search) ?>">
                <button type="submit">Search</button>
                <?php if ($search): ?>
                    <a href="?i=audio" class="clear-search">Clear</a>
                <?php endif; ?>
            </form>
        </div>

        <div class="results-info">
            Showing <?= $pagination['offset'] + 1 ?> - <?= min($pagination['offset'] + $pagination['perPage'], $total) ?> of <?= $total ?> audio files
        </div>

        <div class="items-list">
            <?php foreach ($audios as $audio): ?>
                <div class="item-card audio-card" style="border-left: 4px solid <?= e($audio['colour']) ?>">
                    <div class="audio-content">
                        <h3><?= e($audio['caption']) ?></h3>
                        <audio controls preload="none">
                            <source src="<?= e($audio['path']) ?>" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                        <div class="meta-info">
                            ID: <?= $audio['id'] ?> | 
                            Submitted: <?= date('Y-m-d H:i', strtotime($audio['submission_time'])) ?>
                            <?php if ($audio['submitter_id']): ?>
                                | By: <?= $audio['submitter_id'] ?>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php if (empty($audios)): ?>
                <p class="no-results">No audio files found.</p>
            <?php endif; ?>
        </div>

        <?php if ($pagination['totalPages'] > 1): ?>
            <div class="pagination">
                <?php if ($page > 1): ?>
                    <a href="?i=audio&page=1<?= $search ? '&search=' . urlencode($search) : '' ?>">&laquo; First</a>
                    <a href="?i=audio&page=<?= $page - 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Previous</a>
                <?php endif; ?>

                <span class="page-info">Page <?= $page ?> of <?= $pagination['totalPages'] ?></span>

                <?php if ($page < $pagination['totalPages']): ?>
                    <a href="?i=audio&page=<?= $page + 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Next</a>
                    <a href="?i=audio&page=<?= $pagination['totalPages'] ?><?= $search ? '&search=' . urlencode($search) : '' ?>">Last &raquo;</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>