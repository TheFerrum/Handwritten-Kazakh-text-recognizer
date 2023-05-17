function _(selector){
    return document.querySelector(selector);
}


var marks = [];
var pencil;
// var isFirstLine = true;

function setup(){
    let canvas = createCanvas(1000, 650);
    canvas.parent("canvas-wrapper");
    background(255);
    // var penSizeInput = select("#pen-size");
    // var penColorInput = select("#pen-color");

    // var penSize = parseInt(penSizeInput.value());
    // var penColor = penColorInput.value();
    // pencil = new Marker(penSize, penColor);
    // penSizeInput.changed(updatePenSize);
    // penColorInput.changed(updatePenColor);
}

// function draw() {
//     background(255);
//     pencil.displayMarkings();
// }

// function mousePressed() {
//     pencil.startDrawing();
// }
  
// function mouseReleased() {
//     pencil.stopDrawing();
// }

// function mouseDragged() {
//     pencil.draw(mouseX, mouseY);
// }

// function updatePenSize() {
//     var newSize = parseInt(this.value());
//     pencil.setSize(newSize);
// }
  
// function updatePenColor() {
//     var newColor = this.value();
//     pencil.setColor(newColor);
// }

function mouseDragged(){
    let size = parseInt(_("#pen-size").value);
    let color = _("#pen-color").value;
    fill(color);
    stroke(color);
    strokeWeight(1);
    ellipse(mouseX, mouseY, size, size);
}

function clearCanvas(){
    background(255);
}

document.addEventListener("DOMContentLoaded", function() {
    _("#clear-canvas").addEventListener("click", function () {
        clearCanvas();
    });
});
  
document.addEventListener("DOMContentLoaded", function() {
    _("#save-canvas").addEventListener("click", function () { 
        let canvas = document.getElementById("defaultCanvas0");
        canvas.toBlob(function(blob) {
            let formData = new FormData();
            formData.append("image", blob, 'sketch.png');  // use the current save count in the filename
            // append the CSRF token to the form data
            let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            formData.append("csrfmiddlewaretoken", csrfToken);

            fetch("save-canvas/", {
                method: "POST",
                body: formData,
                credentials: "include",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            }).then(response => {
                // handle the response here
                if (!response.ok) {
                    throw new Error("Failed to save canvas image.");
                }
            }).catch(error => {
                // handle errors here
                console.error(error);
            });
            
        }, "image/png");
    });
}); 

document.addEventListener("DOMContentLoaded", function() {
    _("#predict-canvas").addEventListener("click", function () { 
        let canvas = document.getElementById("defaultCanvas0");
        canvas.toBlob(function(blob) {
            let formData = new FormData();
            formData.append("image", blob, 'sketch.png');  // use the current save count in the filename
            // append the CSRF token to the form data
            let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            formData.append("csrfmiddlewaretoken", csrfToken);

            fetch("predict-canvas/", {
                method: "POST",
                body: formData,
                credentials: "include",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                let prediction = data.prediction;
                _(".result h1").innerHTML = `Your prediction is: ${prediction}`;
            })
            .catch(error => console.error(error));
        }, "image/png");
    });
});

document.addEventListener("DOMContentLoaded", function() {
    _("#send-img").addEventListener("click", function () {
        let input = document.getElementById('image-input');
        let file = input.files[0];

        // Create a FormData object and add the file to it
        let formData = new FormData();
        formData.append('image', file);

        let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        formData.append("csrfmiddlewaretoken", csrfToken);

        // Send a POST request to the server using the Fetch API
        fetch('predict-canvas/', {
            method: 'POST',
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            // Update the h1 element with the new response
            let prediction = data.prediction;
            _(".result h1").innerHTML = `Your prediction is: ${prediction}`;
        })
        .catch(error => console.error(error));
    });
});