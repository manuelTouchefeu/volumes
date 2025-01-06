"use strict";

var finished = document.querySelector('#finished');
var submit = document.querySelector('#submit');

var s_id = document.querySelector("#s_id").value;
console.log(s_id);

finished.addEventListener('change', function(e) {
    var status = finished.value;
    console.log(status);
    var json = {'s_id': s_id, 'action': 'finished', 'status': status}
    json = JSON.stringify(json);
    var xhr = new XMLHttpRequest();
    // Envoi de la requête.
    var host = window.location.origin + '/update_series';
    xhr.open('POST', host);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(json);

    // Réception des données.
    xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === xhr.DONE) {
            var response = xhr.responseText;
            console.log(response);
        }
    }, false);
}, false);

submit.addEventListener('click', function(e) {
    var json = {'s_id': s_id, 'action': 'title', title: document.querySelector('#title').value}
    json = JSON.stringify(json);
    var xhr = new XMLHttpRequest();
    // Envoi de la requête.
    var host = window.location.origin + '/update_series';
    xhr.open('POST', host);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(json);

    // Réception des données.
    xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === xhr.DONE) {
            var response = JSON.parse(xhr.responseText);
            console.log(response['title']);
            document.querySelector('h1').innerText = response['title']
        }
    }, false);
}, false);



