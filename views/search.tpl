% rebase('base.tpl')

<form action="/search" method="post" id="search" autocomplete="off">
    <label for="isbn">isbn:</label> <br>
    <input id="isbn" name="isbn" type="text" value="{{ form['isbn'] }}"/> <br>
    <label for="author">auteur:</label> <br>
    <input id="author" name="author" type="text" value="{{ form['author'] }}"/> <br>
    <label for="title">titre:</label> <br>
    <input id="title" name="title" type="text" value="{{ form['title'] }}"/> <br>
    <label for="publisher">éditeur:</label> <br>
    <input id="publisher" name="publisher" type="text" value="{{ form['publisher'] }}"/> <br>
    
    <label for="date">année de publication:</label> <br>
    <input id="date" name="date" type="text" value="{{ form['date'] }}"/> <br>

    <label for="dewey">sujet:</label> <br>
    <input id="dewey" name="dewey" type="text" value="{{ form['dewey'] }}"/> <br>
    <label for="comment">commentaire:</label> <br>
    <input id="comment" name="comment" type="text" value="{{ form['comment'] }}"/> <br>
    <br>
    <input name="bouton" type="submit" value="Valider"/>
</form>

% if books:   
    % if books.__len__() > 1:
        <p id="info">{{ books.__len__() }} résultats. <span id="export">Exporter la liste.</span></p>
    % elif books.__len__() == 1:
        <p id="info">{{ books.__len__() }} résultat. <span id="export">Exporter la liste.</span></p>
    % end
    % for book in books:  
       <p><a href="/book/{{book.id_book}}">
            {{ ", ".join([b.__str__() for b in book.authors]) }}
            % if book.series is not None:
            | {{ book.series.title }}
            % end
            | <span class="title">{{ book.title }}</span> | {{ book.publisher.name }} | {{ book.date }}</a> | <span id="b_{{ book.id_book }}" class="button">X</span>
       </p>
    % end
% end

<script src="/static/js/search.js"></script>
