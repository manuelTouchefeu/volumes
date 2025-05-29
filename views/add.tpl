% rebase('base.tpl')


% if book is not None:
    <p>Le livre '{{ book.title }}' a bien été enregistré.</p>
% end

<form id="add_form" action="/add" method="post" autocomplete="off">
    <label for="isbn">isbn:</label> <br>
    <input id="isbn" name="isbn" type="text" placeholder="{{ form['isbn'] }}"/>  <input type="button" id="googleBooks" value="Chance"> <br>
    <label for="category">categorie:</label> <br>
    <select id="category" name="category">
        <option value="-">-</option>
        % for item in categories:
            <option value={{ item.index }}>{{ item.index }} - {{ item.description[0:100] }}</option>
        % end
    </select><br>
    <label for="author">auteur:</label> <br>
    <input id="author" name="author" list="suggestAuthor" type="text" placeholder="{{ form['author'] }}"/>  <span id="plus"><strong>+</strong></span><br>
    <datalist id="suggestAuthor"></datalist>
    <label for="title">titre:</label> <br>
    <input id="title" name="title" type="text" placeholder="{{ form['title'] }}"/> <br>
    <label for="series">serie:</label> <br>
    <input id="series" name="series" list="suggestSeries" type="text" placeholder="{{ form['series'] }}"/> <br>
    <datalist id="suggestSeries"></datalist>
    <label for="publisher">éditeur:</label> <br>
    <input id="publisher" name="publisher" list="suggestPublisher" type="text" placeholder="{{ form['publisher'] }}"/> <br>
    <datalist id="suggestPublisher"></datalist>
    <label for="date">date:</label> <br>
    <input id="date" name="date" type="text" placeholder="{{ form['date'] }}"/> <br>
    <label for="description">description:</label> <br>
    <textarea id="description" name="description" rows="10" cols="50" placeholder="{{ form['description'] }}"></textarea>
    <br>
    <label for="annotation">annotation:</label> <br>
    <input id="annotation" name="annotation" type="text" placeholder="{{ form['annotation'] }}"/> <br>
    <br>
    <input name="bouton" type="submit" value="Valider"/>
</form>

% if cover is not None:
        <img class="cover" src="{{ cover }}" alt=""/>
% end

<script src="/static/js/add_book.js"></script>
