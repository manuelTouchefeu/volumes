"use strict";

window.addEventListener('load' , function() {
    var canvas = document.getElementById('logo');
    if(!canvas) {
        alert("Impossible de récupérer le canvas");
        return;
    }
    var context = canvas.getContext('2d');
    if(!context) {
        alert("Impossible de récupérer le context du canvas");
        return;
    }

    var long = 0;
    function animate() {
        if(long<0.6) {
            long+=0.05;
            context.clearRect(0, 0, canvas.width, canvas.height)
            context.fillStyle = "rgb(200,0,0)";
            context.fillRect (0, 0, 50, 50);
            context.fillStyle = "rgba(0, 0, 200," + long +  ")";
            context.fillRect (25, 25, 50, 50);
            context.strokeRect (25, 25, 50, 50);
            context.strokeRect (25, 25, 50, long);
        }
    }

    var myInterval = setInterval(animate, 1000/30); //Notre boucle de rafraîchissement.

}, false);
