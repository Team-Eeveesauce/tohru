
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="pages/style.css">
<?php
// index.php - Main landing page
require_once 'pages/config.php';

$page = $_GET['page'] ?? 'home';
$allowed_pages = ['home', 'quotes', 'tips', 'stuff', 'images', 'audio', 'pools'];
$page = in_array($page, $allowed_pages) ? $page : 'home';

if ($page !== 'home') {
    include "pages/{$page}.php";
    exit;
}
?>
    <title>Tohru Database Browser</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>Tohru Database Browser</h1>
            <p>Browse and search Discord bot data</p>
        </header>

        <nav class="main-nav">
            <div class="nav-grid">
                <a href="?page=quotes" class="nav-card">
                    <h3>💬 Quotes</h3>
                    <p>Browse submitted quotes</p>
                </a>

                <a href="?page=tips" class="nav-card">
                    <h3>💡 Tips</h3>
                    <p>View helpful tips</p>
                </a>
                
                <a href="?page=stuff" class="nav-card">
                    <h3>📦 Stuff</h3>
                    <p>Explore categorized items</p>
                </a>
                
                <a href="?page=images" class="nav-card">
                    <h3>🖼️ Images</h3>
                    <p>Image archives</p>
                </a>
                
                <a href="?page=audio" class="nav-card">
                    <h3>🔊 Audio</h3>
                    <p>Audio archives</p>
                </a>
                
                <a href="?page=pools" class="nav-card">
                    <h3>🗂️ Pools</h3>
                    <p>Content collections</p>
                </a>
            </div>
        </nav>
    </div>
</body>
</html>