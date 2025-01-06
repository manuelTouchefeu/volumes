% rebase('base.tpl')

<h1>{{ book.title }}</h1>


<table>
    % if book.isbn is not None:
    <tr>
        <td>Isbn: </td>
        <td>{{ book.isbn }}</td>
    </tr>
    % end
    % if book.series is not None:
    <tr>
        <td>Série: </td>
        <td><a href="/series/{{ book.series.id }}">{{ book.series.title }} (Série
        % if book.series.finished == 1:
         finie)
        % elif book.series.finished == 0:
         en cours)
        % else:
            incomplète)
        % end
        </a></td>
    </tr>
    % end
    <tr>
        <td>Auteur(s): </td>
        <td>{{ ", ".join([b.__str__() for b in book.authors]) }}</td>
    </tr>
    <tr>
        <td>Éditeur: </td>
        <td>{{ book.publisher.name }}</td>
    </tr>
    <tr>
        <td>Année de publication:</td>
        <td>{{ book.date }}</td>
    </tr>
    <tr>
        <td>Classement: </td>
        <td>{{ book.category.index }} - {{ book.category.description }}</td>
    </tr>
    % if book.annotation is not None:
    <tr>
        <td>Info édition: </td>
        <td>{{ book.annotation }}</td>
    </tr>
    % end
</table>

<br>
    % if book.description is not None:
    % txt = book.description.replace("\n", "<br>")
    {{!txt}}
    % end
<br>
<br>
<p class="button" id="back">&lt&ltRetour</p>
<p class="button" id="modif">&gt&gtModifier</p>

<form id="add_form" action="/update/{{ book.id_book }}" method="POST" style="display:None">
    <label for="isbn">isbn:</label> <br>
    % isbn = "" if book.isbn is None else book.isbn
    <input id="isbn" name="isbn" type="text" value="{{ isbn }}"/> <input type="button" id="googleBooks" value="Chance"> <br>
    <label for="category">categorie:</label> <br>
    <select id="category" name="category">
        <option value="-">-</option>
        % for item in categories:
            % if item.description == book.category.description:
                <option value={{ item.index }} selected>{{ item.index }} - {{ item.description[0:100] }}</option>
            % else:
                <option value={{ item.index }}>{{ item.index }} - {{ item.description[0:100] }}</option>
            % end
        % end
    </select><br>
    <label for="author">auteur:</label> <br>
    % lastInputIndex = 0
    % for index, author in enumerate(book.authors):
        % name = "%s, %s" % (author.last_name, author.first_name) if author.first_name is not None else author.last_name
        % if index == 0:
            <input id="author" name="author" list="suggestAuthor" type="text" value="{{ name }}"/>
        % else:
            <input id="{{ "authorInput%d" % lastInputIndex }}" name="{{ "authorInput%d" % lastInputIndex }}" class="authorInput" list="suggestAuthor" type="text" value="{{ name }}"/>
            % lastInputIndex += 1
        % end
    % end
    <span id="plus"><strong>+</strong></span><br>
    <datalist id="suggestAuthor"></datalist>
    <label for="title">titre:</label> <br>
    <input id="title" name="title" type="text" value="{{ book.title }}"/> <br>
    <label for="series">serie:</label> <br>
    % title = "" if book.series is None else book.series.title
    <input id="series" name="series" list="suggestSeries" type="text" value="{{ title }}"/> <br>
    <datalist id="suggestSeries"></datalist>
    <label for="publisher">éditeur:</label> <br>
    <input id="publisher" name="publisher" list="suggestPublisher" type="text" value="{{ book.publisher.name }}"/> <br>
    <datalist id="suggestPublisher"></datalist>
    <label for="date">date:</label> <br>
    <input id="date" name="date" type="text" value="{{ book.date }}"/> <br>
    <label for="description">description:</label> <br>
    % description = "" if book.description is None else book.description
    <textarea id="description" name="description" rows="10" cols="50">{{ description }}</textarea>
    <br>
    <label for="annotation">annotation:</label> <br>
    % annotation = "" if book.annotation is None else book.annotation
    <input id="annotation" name="annotation" type="text" value="{{ annotation }}"/> <br>
    <br>
    <input name="bouton" type="submit" value="Valider"/>
</form>

<script src="/static/js/add_book.js"></script>
<script src="/static/js/book.js"></script>
