"use strict";

(function() {
    var more = document.querySelector('#more');
    var offset = 10;
    more.addEventListener('click' , function() {
           // Envoi des données
            var xhr = new XMLHttpRequest();
            var host = window.location.origin + '/'
            xhr.open('POST', host);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.send(JSON.stringify({offset: offset+=10}));
            // Réception des données.
            xhr.addEventListener('readystatechange', function() {
                if (xhr.readyState === xhr.DONE) {
                    console.log(offset);
                    var books = document.querySelector('#books');
                    var response = JSON.parse(xhr.responseText);
                    console.log(response['books']);
                    response['books'].forEach(function (book){
                        var newBook = document.createElement('p');
                        newBook.className = 'book';
                        var newLink = document.createElement('a');
                        newLink.href = '/book/' + book.id;
                        newLink.innerText = book.author + ' | ';
                        if (book.book_series != null) {
                            newLink.innerText += book.book_series + ' | '
                        }
                        newLink.innerText += book.title + ' | ' + book.publisher + ' | ' + book.date
                        newBook.appendChild(newLink);
                        books.appendChild(newBook);
                    });

                }
            }, false);
    }, false);

})();