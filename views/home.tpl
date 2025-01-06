% rebase('base.tpl')

<div id="books">
% for book in books:  
   <p class="book"><a href="/book/{{book.id_book}}">
        {{ ", ".join([b.__str__() for b in book.authors]) }}
        % if book.series is not None:
        | {{ book.series.title }}
        % end
        | {{ book.title }} | {{ book.publisher.name }} | {{ book.date }}</a>
   </p>
% end
</div>

<img id="more"  src="/static/icones/more.png"/>


<script src="/static/js/home.js"></script>
