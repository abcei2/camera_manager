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