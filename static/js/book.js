"use strict";

(function () {
    var plus = document.querySelector('#plus');
    plus.style.display = 'inline';

    var form = document.querySelector('form');

    var back = document.querySelector('#back');
    back.addEventListener('click' , function() {
        history.back();
    }, false);

    var modif = document.querySelector('#modif');
    modif.addEventListener('click' , function() {
        form.style.display = 'block';
    }, false);

})();
