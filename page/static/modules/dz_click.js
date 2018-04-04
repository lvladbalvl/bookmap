    $("#dz").click(function(event) {
        Rx=$(this).position().left;
        Ry=$(this).position().top;
        zcontext.clearRect(0,0,$(this).width(),$(this).height());
        zcontext.beginPath();
        zcontext.moveTo(event.pageX-Rx,event.pageY-Ry);
        zcontext.arc(event.pageX-Rx,event.pageY-Ry,7,0,Math.PI*2);
        zcontext.fillStyle="blue";
        zcontext.fill();
        zcontext.closePath();
        currPoint.x=event.pageX-Rx;
        currPoint.y=event.pageY-Ry;
        dz_filled = true;
    });