<?php
$pdo = getDB();
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$search = isset($_GET['search']) ? trim($_GET['search']) : '';
$poolId = isset($_GET['pool']) ? intval($_GET['pool']) : 0;

// If viewing a specific pool
if ($poolId) {
    $poolStmt = $pdo->prepare("SELECT * FROM pools WHERE id = ? AND visible = 1");
    $poolStmt->execute([$poolId]);
    $pool = $poolStmt->fetch();
    
    if (!$pool) {
        header('Location: pools.php');
        exit;
    }
    
    // Get pool content
    $where = "WHERE pc.pool_id = ? AND pc.visible = 1";
    $params = [$poolId];
    
    if ($search) {
        $where .= " AND pc.content LIKE ?";
        $params[] = "%$search%";
    }
    
    $countStmt = $pdo->prepare("SELECT COUNT(*) FROM pools_content pc $where");
    $countStmt->execute($params);
    $total = $countStmt->fetchColumn();
    
    $pagination = getPagination($total, $page, ITEMS_PER_PAGE);
    
    $stmt = $pdo->prepare("
        SELECT pc.id, pc.content, pc.user_id, pc.timestamp 
        FROM pools_content pc 
        $where 
        ORDER BY pc.timestamp DESC 
        LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
    ");
    $stmt->execute($params);
    $contents = $stmt->fetchAll();
    
} else {
    // List all pools
    $where = "WHERE visible = 1";
    $params = [];
    
    if ($search) {
        $where .= " AND name LIKE ?";
        $params[] = "%$search%";
    }
    
    $countStmt = $pdo->prepare("SELECT COUNT(*) FROM pools $where");
    $countStmt->execute($params);
    $total = $countStmt->fetchColumn();
    
    $pagination = getPagination($total, $page, ITEMS_PER_PAGE);
    
    $stmt = $pdo->prepare("
        SELECT p.*, COUNT(pc.id) as item_count 
        FROM pools p 
        LEFT JOIN pools_content pc ON p.id = pc.pool_id AND pc.visible = 1
        $where 
        GROUP BY p.id
        ORDER BY p.timestamp DESC 
        LIMIT {$pagination['perPage']} OFFSET {$pagination['offset']}
    ");
    $stmt->execute($params);
    $pools = $stmt->fetchAll();
}
?>
    <title><?= $poolId ? e($pool['name']) : 'Pools' ?> - Tohru Database</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>🗂️ <?= $poolId ? e($pool['name']) : 'Pools' ?></h1>
            <a href="<?= $poolId ? '?i=pools' : '<?php echo $basePath; ?>' ?>" class="back-link">
                ← Back to <?= $poolId ? 'Pools' : 'Home' ?>
            </a>
        </header>

        <div class="search-bar">
            <form method="GET" action="">
                <input type="hidden" name="i" value="pools">
                <?php if ($poolId): ?>
                    <input type="hidden" name="pool" value="<?= $poolId ?>">
                <?php endif; ?>
                <input type="text" name="search" placeholder="Search <?= $poolId ? 'content' : 'pools' ?>..." value="<?= e($search) ?>">
                <button type="submit">Search</button>
                <?php if ($search): ?>
                    <a href="?i=pools<?= $poolId ? '&pool=' . $poolId : '' ?>" class="clear-search">Clear</a>
                <?php endif; ?>
            </form>
        </div>

        <div class="results-info">
            Showing <?= $pagination['offset'] + 1 ?> - <?= min($pagination['offset'] + $pagination['perPage'], $total) ?> of <?= $total ?> <?= $poolId ? 'items' : 'pools' ?>
        </div>

        <?php if ($poolId): ?>
            <!-- Pool content view -->
            <div class="pool-info">
                <p><strong>Owner:</strong> <?= $pool['user_id'] ?> | 
                <strong>Created:</strong> <?= date('Y-m-d H:i', strtotime($pool['timestamp'])) ?></p>
            </div>
            
            <div class="items-list">
                <?php foreach ($contents as $content): ?>
                    <div class="item-card pool-content-card">
                        <div class="content-display">
                            <p><?= e($content['content']) ?></p>
                        </div>
                        <div class="meta-info">
                            ID: <?= $content['id'] ?> | 
                            Added by: <?= $content['user_id'] ?> | 
                            <?= date('Y-m-d H:i', strtotime($content['timestamp'])) ?>
                        </div>
                    </div>
                <?php endforeach; ?>

                <?php if (empty($contents)): ?>
                    <p class="no-results">No content found in this pool.</p>
                <?php endif; ?>
            </div>
        <?php else: ?>
            <!-- Pools list view -->
            <div class="items-list">
                <?php foreach ($pools as $p): ?>
                    <div class="item-card pool-card">
                        <div class="pool-header">
                            <h3><a href="?i=pools&pool=<?= $p['id'] ?>"><?= e($p['name']) ?></a></h3>
                            <span class="item-count"><?= $p['item_count'] ?> items</span>
                        </div>
                        <div class="meta-info">
                            ID: <?= $p['id'] ?> | 
                            Owner: <?= $p['user_id'] ?> | 
                            Created: <?= date('Y-m-d H:i', strtotime($p['timestamp'])) ?>
                        </div>
                    </div>
                <?php endforeach; ?>

                <?php if (empty($pools)): ?>
                    <p class="no-results">No pools found.</p>
                <?php endif; ?>
            </div>
        <?php endif; ?>

        <?php if ($pagination['totalPages'] > 1): ?>
            <div class="pagination">
                <?php 
                $queryParams = [];
                if ($search) $queryParams[] = 'search=' . urlencode($search);
                if ($poolId) $queryParams[] = 'pool=' . $poolId;
                $queryString = $queryParams ? '&' . implode('&', $queryParams) : '';
                ?>
                
                <?php if ($page > 1): ?>
                    <a href="?i=pools&page=1<?= $queryString ?>">&laquo; First</a>
                    <a href="?i=pools&page=<?= $page - 1 ?><?= $queryString ?>">Previous</a>
                <?php endif; ?>

                <span class="page-info">Page <?= $page ?> of <?= $pagination['totalPages'] ?></span>

                <?php if ($page < $pagination['totalPages']): ?>
                    <a href="?i=pools&page=<?= $page + 1 ?><?= $queryString ?>">Next</a>
                    <a href="?i=pools&page=<?= $pagination['totalPages'] ?><?= $queryString ?>">Last &raquo;</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>