/// BUTTONS ZONE
let train_button = document.getElementById("train_button")
train_button.onclick = function(ev) {
    console.log(DATA.URL_UPDATE_FACE_MODEL)
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

let capture_button = document.getElementById("capture_button")
capture_button.onclick = function(ev) {
    if(selected_task.value == "detect"){
        detection_context_aux.drawImage(player, 0, 0, detection_canvas_aux.width, detection_canvas_aux.height);
        image = detection_canvas_aux.toDataURL(image_format);
    
        $.post(DATA.URL_GET_DETECTIONS, {id_cam:DATA.id_cam, img: image})
            .done(function(response) {
                let img = new Image()
                img.src = response.img
                img.onload = () => detection_context.drawImage(
                    img, 0, 0, detection_canvas.width, detection_canvas.height)
    
            })
            .fail((response, textStatus, error) => {
                console.log(response, textStatus, error)
            })
    
    }else if(selected_task.value == "register"){
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
    }
    
    //SEND IMAGE AND SAVE WITH NAME
}