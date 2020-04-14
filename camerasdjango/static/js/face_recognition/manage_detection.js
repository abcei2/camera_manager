let DATA = JSON.parse(document.getElementById('data').textContent);


let web_container = document.getElementById("web_container")
let player_mobile = document.getElementById("player_mobile")
let player = document.getElementById('player');

let capture_button = document.getElementById("capture_button")

const constraints = {
    video: {
        facingMode: 'environment'
    },
    audio: false
};



let face_to_register = document.getElementById("face_to_register")
let faces_registered_list = document.getElementById("faces_registered_list")
let face_selection = -1
let face_name_selection = "unknown"

let is_mobile = false

let selected_task = document.getElementById("selected_task")

if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    is_mobile = true

    web_container.hidden = true
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

                        if (schedule_task) setTimeout(identifyFace, 500)
                    })
                    .fail((response, textStatus, error) => {
                        console.log(response, textStatus, error)
                    })
            }

        };
    });

} else {
    web_container.hidden = false
    player_mobile.hidden = true
    capture_button.hidden = false
}

for (let i = 0; i < DATA.faces_registered.length; i++) {
    let listItem = document.createElement("li")
    listItem.className = "list-group-item list-group-item-dark"
    listItem.textContent = DATA.faces_registered[i]
    listItem.tabIndex = "1"
    faces_registered_list.appendChild(listItem)
}

//SELECT FACE ON LIST
faces_registered_list.onclick = function(event) {
    let target = event.target
    if (face_selection != -1)
        faces_registered_list.childNodes[face_selection + 1].className = "list-group-item list-group-item-dark"

    face_selection = $(target).index()
    face_name_selection = faces_registered_list.childNodes[face_selection + 1].textContent
    faces_registered_list.childNodes[face_selection + 1].className = "list-group-item active"
    DATA_OUT_AUX = {
        'face_name': face_name_selection
    }
    $.getJSON(DATA.URL_GET_FACES_IMAGES, DATA_OUT_AUX)
        .done(function(response) {
            let counter_imgs = 0
            for (let i = 0; i < response.images.length; i++) {
                let img = new Image(); // Create new img element
                img.onload = function() {
                    if (counter_imgs == 0)
                        context.drawImage(this, 0, 0, canvas.width, canvas.height);
                    else if (counter_imgs == 1)
                        context1.drawImage(this, 0, 0, canvas1.width, canvas1.height);
                    else if (counter_imgs == 2)
                        context2.drawImage(this, 0, 0, canvas2.width, canvas2.height);
                    else if (counter_imgs == 3)
                        context3.drawImage(this, 0, 0, canvas3.width, canvas3.height);
                    counter_imgs = counter_imgs + 1
                }
                img.src = response.images[i]
            }
        })
        .fail(function(response, textStatus, error) {
            console.log(response, textStatus, error)
        })
}

let container_ip_cam = document.getElementById("container_ip_cam")
let container_web_cam = document.getElementById("container_web_cam")

let image = document.getElementById("img")
let canvas = document.getElementById("myCanvas")
let canvas1 = document.getElementById("myCanvas1")
let canvas2 = document.getElementById("myCanvas2")
let canvas3 = document.getElementById("myCanvas3")


let detection_canvas = document.getElementById("detection_canvas")
let detection_canvas_aux = document.getElementById("detection_canvas_aux")

let register_containter = document.getElementById("register_containter")
let detection_containter = document.getElementById("detection_containter")

const context = canvas.getContext('2d');
const context1 = canvas1.getContext('2d');
const context2 = canvas2.getContext('2d');
const context3 = canvas3.getContext('2d');
const detection_context = detection_canvas.getContext('2d');
const detection_context_aux = detection_canvas_aux.getContext('2d');

let counter_context = 0
let image_format = "image/png"
let schedule_task = false

const identifyFace = async () => {
    detection_context_aux.drawImage(player, 0, 0, detection_canvas_aux.width, detection_canvas_aux.height);
    image = detection_canvas_aux.toDataURL(image_format);

    $.post(DATA.URL_GET_DETECTIONS, {img: image})
        .done(function(response) {
            let img = new Image()
            img.src = response.img
            img.onload = () => detection_context.drawImage(
                img, 0, 0, detection_canvas.width, detection_canvas.height)

            if (schedule_task) setTimeout(identifyFace, 0)
        })
        .fail((response, textStatus, error) => {
            console.log(response, textStatus, error)
        })

}

if (DATA.is_web_cam) {

    /// BUTTONS ZONE
    let train_button = document.getElementById("train_button")
    train_button.onclick = function(ev) {
        $.getJSON(DATA.URL_UPDATE_FACE_MODEL)
            .fail(function(response, textStatus, error) {
                console.log(response, textStatus, error)
            })
    }
    let delete_face_button = document.getElementById("delete_face_button")
    delete_face_button.onclick = function(ev) {
        if (face_selection != -1) {
            item_selected = faces_registered_list.childNodes[face_selection + 1]
            DATA_OUT_AUX = {
                'face_name': item_selected.textContent
            }

            $.getJSON(DATA.URL_DELETE_FACES_IMAGES, DATA_OUT_AUX)
                .done(function(response) {
                    faces_registered_list.removeChild(item_selected)
                })
                .fail(function(response, textStatus, error) {
                    console.log(response, textStatus, error)
                })
        }
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

    let register_button = document.getElementById("register_button")
    register_button.onclick = function(ev) {
        if (counter_context == 4) {
            face_data = {
                face_name: face_to_register.value,
                images: [
                    canvas.toDataURL(image_format),
                    canvas1.toDataURL(image_format),
                    canvas2.toDataURL(image_format),
                    canvas3.toDataURL(image_format)
                ]
            }

            $.post(DATA.URL_ADD_NEW_FACE, face_data)
                .fail(function(response, textStatus, error) {
                    console.log(response, textStatus, error)
                })

            let listItem = document.createElement("li")
            listItem.className = "list-group-item list-group-item-dark"
            listItem.textContent = face_to_register.value
            listItem.tabIndex = "1"
            faces_registered_list.appendChild(listItem)
        }
    }

    //MANAGE VISIBILITY
    container_ip_cam.hidden = true
    container_web_cam.hidden = false
    if (!is_mobile) {
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => player.srcObject = stream)
            .catch(err => console.log(err))
    }

    if (selected_task.value == "register") {
        register_button.hidden = false
        detection_containter.hidden = true
        register_containter.hidden = false
        capture_button.disabled = false
        if (counter_context == 4) {
            face_to_register.disabled = false
        }
        schedule_task = false
    } else if (selected_task.value == "detect") {
        if (!is_mobile) {
            schedule_task = true
            setTimeout(identifyFace, 0)
        }
        register_button.hidden = true
        detection_containter.hidden = false
        register_containter.hidden = true
        capture_button.disabled = true
        face_to_register.disabled = true
    }

    selected_task.addEventListener('change', function(ev) {
        if (this.value == "register") {
            detection_containter.hidden = true
            register_containter.hidden = false
            capture_button.disabled = false
            if (counter_context == 3) {
                face_to_register.disabled = false
            }
            schedule_task = false
        } else if (this.value == "detect") {
            if (!is_mobile) {
                schedule_task = true
                setTimeout(identifyFace, 0)
            }
            detection_containter.hidden = false
            register_containter.hidden = true
            capture_button.disabled = true
            face_to_register.disabled = true
        }
    })

} else {
    let toggle_url = false
    let edit_url_button = document.getElementById("edit_url_button")
    let url_cam = document.getElementById("url_cam")
    container_ip_cam.hidden = false
    container_web_cam.hidden = true

    url_cam.value = DATA.url

    edit_url_button.onclick = function() {


        if (toggle_url) {
            edit_url_button.innerHTML = gettext("Edit url")
            DATA.url = url_cam.value
            image.src = url_cam.value

            toggle_url = false
            url_cam.disabled = true


            $.getJSON(DATA.URL_EDIT, DATA)
                .fail(function(response, textStatus, error) {
                    console.log(response, textStatus, error)
                })
        } else {
            edit_url_button.innerHTML = gettext("Save url")
            toggle_url = true
            url_cam.disabled = false
        }
    }
}
