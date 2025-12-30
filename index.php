
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="pages/style.css">
<?php
// index.php - Main landing page
require_once 'pages/config.php';

$page = $_GET['i'] ?? 'home';
$allowed_pages = ['home', 'quotes', 'tips', 'stuff', 'images', 'audio', 'pools'];
$page = in_array($page, $allowed_pages) ? $page : 'home';

if ($page !== 'home') {
    include "pages/{$page}.php";
    exit;
}
?>
    <title>TohruDB Web Browser Solution</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>TohruDB Web Browser Solution</h1>
            <p>I know this UI sucks ass but it's better than no UI. Thanks, Claude.</p>
        </header>

        <nav class="main-nav">
            <div class="nav-grid">
                <a href="?i=quotes" class="nav-card">
                    <h3>💬 Quotes</h3>
                    <p>Browse submitted quotes</p>
                </a>

                <a href="?i=tips" class="nav-card">
                    <h3>💡 Tips</h3>
                    <p>View helpful tips</p>
                </a>
                
                <a href="?i=stuff" class="nav-card">
                    <h3>📦 Stuff</h3>
                    <p>Explore categorized items</p>
                </a>

                <a href="?i=images" class="nav-card">
                    <h3>🖼️ Images</h3>
                    <p>Image archives</p>
                </a>
                
                <a href="?i=audio" class="nav-card">
                    <h3>🔊 Audio</h3>
                    <p>Audio archives</p>
                </a>
                
                <a href="?i=pools" class="nav-card">
                    <h3>🗂️ Pools (Beta)</h3>
                    <p>Content collections</p>
                </a>
            </div>
        </nav>
    </div>
</body>
</html>