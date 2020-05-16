
container_ip_cam.hidden = true
container_web_cam.hidden = false

let capture_button = document.getElementById("capture_button")
const constraints = {
    video: {
        facingMode: 'environment'
    },
    audio: false
};

if (!is_mobile) {
    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => player.srcObject = stream)
        .catch(err => console.log(err))
}

capture_button.onclick = function(ev) {
    if (counter_context == 0) {
        context.drawImage(player, 0, 0, canvas.width, canvas.height)
        counter_context = counter_context + 1
        image = canvas.toDataURL(image_format)
    } else if (counter_context == 1) {
        context1.drawImage(player, 0, 0, canvas1.width, canvas1.height)
        counter_context = counter_context + 1
        image = canvas1.toDataURL(image_format)
    } else if (counter_context == 2) {
        context2.drawImage(player, 0, 0, canvas2.width, canvas2.height)
        counter_context = counter_context + 1
        image = canvas2.toDataURL(image_format)
    } else if (counter_context == 3) {
        context3.drawImage(player, 0, 0, canvas3.width, canvas3.height)
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
    //SEND IMAGE AND SAVE WITH NAME
}

