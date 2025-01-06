% rebase('base.tpl')

<h1>{{ s.title }}</h1>

% for book in s.books:
   <p><a href="/book/{{book.id_book}}">
        {{ ", ".join([b.__str__() for b in book.authors]) }}
        | {{ book.title }} | {{ book.publisher.name }} | {{ book.date }}</a>
   </p>
% end

<p class="button" id="back">&lt&ltRetour</p>


<input type="hidden" id="s_id" value="{{ s.id }}">

<div>
    <label for="finished">Statut de la série</label>
    <select id="finished" name="finished">
      % if s.finished == 0:
        <option value="0" selected>En cours</option>
      %  else:
        <option value="0">En cours</option>
      % end
      % if s.finished == 1:
        <option value="1" selected>Finie</option>
      % else:
        <option value="1">Finie</option>
      % end
      % if s.finished == 2:
        <option value="2" selected>Incomplète</option>
      % else:
        <option value="2">Incomplète</option>
      % end
    </select>
</div>
<br>
<div>
    <label for="title">Modifier le nom: </label>
    <input type="text" name="title" id="title" value="{{ s.title }}">
    <input type="button" id="submit" name="submit" value="Valider">
</div>

<script src="/static/js/series.js"></script>
