function _(selector){
    return document.querySelector(selector);
}

function setup(){
    const sketchContainer = document.getElementById('canvas-wrapper');
    const canvas = createCanvas(1000,650);
    canvas.parent('canvas-wrapper');
    sketch = select('#canvas-wrapper canvas');

    penSizeInput = select('#pen-size');
    penColorInput = select('#pen-color');

    background(255);
}

function draw() {
    if (mouseIsPressed) {
      const penSize = penSizeInput.value();
      const penColor = penColorInput.value();

      stroke(penColor);
      strokeWeight(penSize);
      line(pmouseX, pmouseY, mouseX, mouseY);
    }
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


function deleteImage(imageName) {
    var csrftoken = getCookie('csrftoken'); 
    $.ajax({
      url: '/images/delete-image/', // Replace with the actual URL of your Django backend function
      type: 'POST',
      headers: {
        'X-CSRFToken': csrftoken // Include the CSRF token in the request headers
      },
      data: {
        image_name: imageName
      },
      success: function(response) {
        console.log(response); // Print the image name returned by the Django backend
        location.reload();
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }