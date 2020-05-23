
container_ip_cam.hidden = true
container_web_cam.hidden = false

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



