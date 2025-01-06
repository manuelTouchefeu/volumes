<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8" />
        <link rel="stylesheet" href="/static/css/volumes.css" />
		<title>Volumes</title>
	</head>

	<body>

        <header>
            <div id="login">
                <a href="/logout">Logout</a>
            </div>
            <nav id="navbar">
                <ul>
                    <li><a href="/">Nouveautés</a></li>
                    <li><a href="/search">Recherche</a></li>
                    <li><a href="/add">Ajouter un livre</a></li>
                    <li><a href="/series_all/all">Séries</a></li>
                    <li><a href="/categories">Catégories</a></li>
                </ul>
            </nav>
            <canvas id="logo" width="100" height="100"></canvas>
        </header>

        <section id="content">
            {{!base}}
        </section>

        <script src="/static/js/draw.js"></script>
        <script src="/static/js/base.js"></script>
	</body>
</html>
