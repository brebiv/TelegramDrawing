function init() {
    var sketchpad = new Sketchpad({
        element: '#panel',
        width: window.innerWidth,
        height: window.innerHeight,
    });
}

function toPNG() {
    var hash = window.location.pathname.substr(1)   // path is /{hash}, so I'm removing first chat which is /
    console.log(hash)
    var canvas = document.getElementById("panel");
    var imgURL = canvas.toDataURL("image/png");


    $.ajax({
        type: "POST",
        url: "/getImage/"+hash,
        data: imgURL
      }).done(function(o) {
        console.log('saved');
        window.close()
      });
}
