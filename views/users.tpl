<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="/static/css/volumes.css" />
		<title>Volumes</title>
	</head>

	<body>
        <header>
            
        </header>

        <section id="content">
           <h1>Utilisateurs</h1>
            <ul>
            % for u in users:
                <li id="{{u.id}}">{{u}} | {{u.login}} | <span class="supp">X</span></li>
            % end
            </ul>

            <h2>Ajouter un utilisateur:</h2>
                <form method="post" action="/add_user">
                    <label for="last_name">Nom:</label> <br>
                    <input id="last_name" name="last_name" type="text"/> <br>
                    <label for="first_name">Prénom:</label> <br>
                    <input id="first_name" name="first_name" type="text"/> <br>
                    <label for="login">Login:</label> <br>
                    <input id="login" name="login" type="text"/> <br>
                    <label for="password">Mot de passe :</label> <br>
                    <input id="password" name="password" type="text"/> <br>
                    <br>
                    <input id="submit" type="submit" value="Envoyer"/>
                </form>
        </section>
	</body>
</html>
