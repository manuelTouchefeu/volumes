"use strict";

// export
(function() {
    
    var exprt = document.querySelector('#export');
    if (exprt) {
        exprt.addEventListener('click' , function() {
            var inputs = document.querySelectorAll("input[type='text']");
            var json = {};
            for (var i=0, l=inputs.length; i<l; i++) {
                if (inputs[i].value.length > 0) {
                    json[inputs[i].name] = inputs[i].value;
                }
            }
            json = JSON.stringify(json);
            // Envoi des données
            var xhr = new XMLHttpRequest();
            var host = window.location.origin + '/export'
            xhr.open('POST', host);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.send(json);
            // Réception des données.
            xhr.addEventListener('readystatechange', function() {
                if (xhr.readyState === xhr.DONE) {
                    var response = xhr.responseText;
                    if (response == "ok") {
                        var link = document.createElement("a");
                        link.href = "/static/export.csv";
                        link.innerText = " -> download";
                        document.querySelector("#info").appendChild(link);
                    }
                }
            }, false);
        }, false);
    }
})();

// del
(function() {

    function rmv(button) {
        button.addEventListener('click' , function() {
            if (confirm("Supprimer \"" + this.parentNode.querySelector(".title").innerText + "\"?")) {
                var xhr = new XMLHttpRequest();
                var host = window.location.origin + '/del'
                xhr.open('POST', host);
                xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xhr.send(JSON.stringify({id: this.id}));
                // Réception des données.
                xhr.addEventListener('readystatechange', function() {
                    if (xhr.readyState === xhr.DONE) {
                        var response = xhr.responseText;
                        if (response == "ok") {
                            var title = button.parentNode.querySelector(".title").innerText;
                            button.parentNode.remove();
                            var az = document.getElementById("info");
                            az.innerText = 'Le livre "' + title + '" a été supprimé.';   
                        }
                    }
                }, false);
            }
        }, false);
    }
    var buttons = document.querySelectorAll('.button');
    for (var i=0, l=buttons.length; i<l; i++) {
        rmv(buttons[i]);
    }

})();
