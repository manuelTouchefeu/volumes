"use strict";

function suggest(input, dataList, table) {

    var input = document.getElementById(input);
    var dataList = document.getElementById(dataList);
    input.addEventListener('keyup' , function help() {

        // Au moins 2 caractères sont recherchés.
        if (input.value.length > 1){
            var content = input.value;
            var xhr = new XMLHttpRequest();
            // Envoi de la requête.
            var host = window.location.origin + '/add_ajax';
            xhr.open('POST', host);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.send('content=' + content + '&table=' + table);
            //xhr.send(JSON.stringify({content: content...}))
            // Réception des données.
            xhr.addEventListener('readystatechange', function() {
                if (xhr.readyState === xhr.DONE) {
                    var response = JSON.parse(xhr.responseText);
                    // Suppression des suggestions existantes.
                    var existSuggest = document.querySelectorAll('form datalist option');
                    for(var i=0; i<existSuggest.length; i++){
                       existSuggest[i].parentNode.removeChild(existSuggest[i]);
                    }
                    // Insertion des suggestions.
                    for(var i=0; i<response.length; i++){
                        // Closure!
                        (function (i) {
                            var newOption = document.createElement('option');
                            var txt = '';
                            if (table == 'author') {
                                txt = response[i].first_name == null ? response[i].last_name : response[i].last_name +', ' + response[i].first_name;
                            }
                            else {
                                txt = table == 'publisher' ? response[i].name : response[i].title;
                            }
                            newOption.value = txt;
                            dataList.appendChild(newOption);
                            var newLinkText = document.createTextNode(txt);
                            newOption.appendChild(newLinkText);
                        })(i);
                    }
                }
            }, false);
        }
        else {
            // Suppression des suggestions existantes.
            var existSuggest = document.querySelectorAll('form datalist option');
            for(var i=0; i<existSuggest.length; i++){
               existSuggest[i].parentNode.removeChild(existSuggest[i]);
            }
        }
    }, false);
}

/* mise à jour de finished pour les séries.
if (table == 'series') {
    var finished = document.getElementById('finished');
    newOption.addEventListener('click', function(e) {
        console.log(finished);
    }, false);
}
*/

suggest('publisher', 'suggestPublisher', 'publisher');
suggest('series', 'suggestSeries', 'series');


// Gestion de l'input Auteur.
(function() {
    
    function createInput(lastInputIndex) {
        var newInput = document.createElement('input');
        newInput.type="text"
        newInput.id = 'authorInput_'+lastInputIndex;
        newInput.name = 'authorInput_'+lastInputIndex;
        newInput.style.display = 'inline';
        newInput.className = 'authorInput';
        newInput.setAttribute('list', 'suggestAuthor');
        return newInput;
    }

    // Chercher les éléments
    var authorInput = document.querySelector('#author'),
        plus = document.querySelector('#plus'),
        form = document.getElementById('add_form');
    var lastInputIndex = 0;
    plus.style.display = 'none';

    // Comportement du premier author
    authorInput.addEventListener('keyup' , function() {
        if (this.value != '') {
            plus.style.display = 'inline';
        }
    }, false);
    // Suggesitions ajax
    suggest('author', 'suggestAuthor', 'author');

    // Comportement du plus > ajouter des inputs.
    plus.addEventListener('mouseover' , function() {
        plus.style.cursor = "pointer";
    }, false);
    plus.addEventListener('click' , function() {
        var newInput = createInput(lastInputIndex++) 
        form.insertBefore(newInput, plus);
        plus.style.display = 'none';
        newInput.addEventListener('keyup' , function() {
            if (this.value != '') {
                plus.style.display = 'inline';
            }
        }, false);      
        suggest(newInput.id, 'suggestAuthor', 'author'); // On ajoute l'évènement datalist (la datalist  est commune).
    }, false);
})();

// quick add
  // https://www.googleapis.com/books/v1/volumes?q=isbn:2203399104
var quickAdd = document.getElementById('googleBooks');
quickAdd.addEventListener('click', function(){
    var isbn = document.querySelector('#isbn');
    isbn.value = isbn.value.replaceAll("-", "");
    console.log(isbn.value);
     if (isbn.value.length != 0 && isbn.value.length != 13 && isbn.value.length != 10) {
        isbn.className = 'incorrect';
        return
    }
    var xhr = new XMLHttpRequest();
    // Envoi de la requête.
    var url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn.value;
    xhr.open('GET', url);
    xhr.send();
    xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === xhr.DONE) {
            var response = JSON.parse(xhr.responseText);
            console.log(xhr.responseText);
            document.getElementById("title").value = response['items'][0]['volumeInfo'].title;
            document.getElementById("description").value = response['items'][0]['volumeInfo'].description;
            document.getElementById("date").value = response['items'][0]['volumeInfo'].publishedDate;
            document.getElementById("publisher").value = response['items'][0]['volumeInfo'].publisher;
            document.getElementById("author").value = response['items'][0]['volumeInfo'].authors.join(';');
            console.log(response['items'][0]['volumeInfo']);
        }
    }, false);
}, false);



// Validation du formulaire
(function() {

    // Fonctions de vérification.
    var check = {};

    check['isbn'] = function() {
        var isbn = document.getElementById('isbn');
        isbn.value = isbn.value.replaceAll("-", "");
        if (isbn.value.length != 0 && isbn.value.length != 13 && isbn.value.length != 10) {
            isbn.className = 'incorrect';
            return false;
        }
        isbn.classList.remove('incorrect');
        return true;
    };

    check['category'] = function() {
        var category = document.getElementById('category');
        if (category.value == '-') {
            category.className = 'incorrect';
            return false;
        }
        category.classList.remove('incorrect');
        return true;
    };

    check['date'] = function() {
        var publicationDate = document.getElementById('date');
        if (isNaN(parseInt(publicationDate.value))) {
            publicationDate.className = 'incorrect';
            return false;
        }
        else {
            var date = new Date();
            if (date.getFullYear() < parseInt(publicationDate.value)) {
                publicationDate.className = 'incorrect';
                return false;
            }
        }
        publicationDate.classList.remove('incorrect');
        return true;
    };

    check['title'] = function() {
        var title = document.getElementById("title");
        if (title.value.length == 0) {
            title.className = 'incorrect';
            return false;
        }
        title.classList.remove('incorrect');
        return true;
    };

    check['publisher'] = function() {
        var publisher = document.getElementById("publisher");
        if (publisher.value.length == 0) {
            publisher.className = 'incorrect';
            return false;
        }
        publisher.classList.remove('incorrect');
        return true;
    };

    check['author'] = function() {
        var author = document.getElementById("author");
        if (author.value.length == 0) {
            author.className = 'incorrect';
            return false;
        }
        author.classList.remove('incorrect');
        return true;
    };

    //Ne rien faire!!!
    check['series'] = function(){return true;}
    check['description'] = check['series'];
    check['annotation'] = check['series'];

    // debut
    var form = document.getElementById('add_form'),
        inputs = document.querySelectorAll('#add_form input[type=text], #add_form select'),
        inputsLength = inputs.length;

    form.addEventListener('submit', function(e) {

        var result = true;
        for (var i in check) {
            result = check[i]() && result;
        }
        if (!result) {
            e.preventDefault();
            return
        }
        // Gestion des auteurs
        var inputsAuthor = document.querySelectorAll('.authorInput');
        var inputsValues = [];
        for (var i=0, c=inputsAuthor.length; i<c; i++) {
            if (inputsAuthor[i].value != '') {
                inputsValues.push(inputsAuthor[i].value);
            }
        }
        if (inputsValues.length > 0) {
            var authorInputValue = inputsValues.join(';');
            var author = document.getElementById("author");
            author.value = author.value + ';' + authorInputValue;
            console.log(author.value);
        }
    }, false);

})();
