
let is_mobile = false
let player_mobile = document.getElementById("player_mobile")
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    is_mobile = true

    player_container.hidden = true
    capture_button.hidden = true
    player_mobile.hidden = false

    let counter_imgs = 0

    player_mobile.addEventListener('change', function(e) {

        let file = e.target.files[0];
        // Do something with the video file.
        let img = new Image()
        img.src = URL.createObjectURL(file);
        img.onload = function() {
            if (selected_task.value == "register") {
                if (counter_context == 0) {
                    context.drawImage(this, 0, 0, canvas.width, canvas.height)
                    counter_context = counter_context + 1
                    image = canvas.toDataURL(image_format)
                } else if (counter_context == 1) {
                    context1.drawImage(this, 0, 0, canvas1.width, canvas1.height)
                    counter_context = counter_context + 1
                    image = canvas1.toDataURL(image_format)
                } else if (counter_context == 2) {
                    context2.drawImage(this, 0, 0, canvas2.width, canvas2.height)
                    counter_context = counter_context + 1
                    image = canvas2.toDataURL(image_format)
                } else if (counter_context == 3) {
                    context3.drawImage(this, 0, 0, canvas3.width, canvas3.height)
                    image = canvas3.toDataURL(image_format)
                    face_to_register.disabled = false
                    counter_context = counter_context + 1
                    this.innerHTML = gettext("Clear images")
                } else {
                    counter_context = 0
                    context.clearRect(0, 0, canvas.width, canvas.height)
                    context1.clearRect(0, 0, canvas1.width, canvas1.height)
                    context2.clearRect(0, 0, canvas2.width, canvas2.height)
                    context3.clearRect(0, 0, canvas3.width, canvas3.height)

                    face_to_register.disabled = true
                    this.innerHTML = gettext("Capture image")
                    return
                }
                counter_imgs = counter_imgs + 1
            } else {

                detection_context_aux.drawImage(this, 0, 0, detection_canvas_aux.width, detection_canvas_aux.height);
                image = detection_canvas_aux.toDataURL(image_format);

                $.post(DATA.URL_GET_DETECTIONS, {
                        img: image
                    })
                    .done(function(response) {
                        let img2 = new Image()
                        img2.src = response.img
                        img2.onload = () => detection_context.drawImage(
                            img2, 0, 0, detection_canvas.width, detection_canvas.height)

                    })
                    .fail((response, textStatus, error) => {
                        console.log(response, textStatus, error)
                    })
            }

        };
    });

} else {
    player_container.hidden = false
    player_mobile.hidden = true
    capture_button.hidden = false
}