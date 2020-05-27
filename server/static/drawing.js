var sketchpad;

function init() {
    colorPicker = document.querySelector("#color-picker");
    colorPicker.addEventListener("change", updateColor, false);
    colorPicker.select();
    sketchpad = new Sketchpad({
        element: '#panel',
        width: window.innerWidth,
        height: window.innerHeight,
    });
}

function updateColor(event) {
    console.log("Color changed")
    sketchpad.color = event.target.value;
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
