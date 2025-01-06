"use strict";

(function() {
    //Afficher les menus
    var url = window.location.href,
        previousUrl =  document.referrer;
    //Couleurs
    var links = document.querySelectorAll('#navbar a');
    for (var i=0, c=links.length; i<c; i++) {
        if (links[i].href == url) {
            links[i].style.color = "rgb(200,0,0)";
        }
        //cas de books_details
        if (url.search('/books/book_details') != -1) {
            if (links[i].href == previousUrl) {
                links[i].style.color = 'rgb(200,0,0)';
                break;
            }
        }
    }
})();


var back = document.querySelector('#back');
if (back != null) {
    back.addEventListener('click' , function() {
        history.back();
    }, false);
}
