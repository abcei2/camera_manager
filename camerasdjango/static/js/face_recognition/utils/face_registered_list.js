

let face_to_register = document.getElementById("face_to_register")
let faces_registered_list = document.getElementById("faces_registered_list")
let face_selection = -1
let face_name_selection = "unknown"


let selected_task = document.getElementById("selected_task")

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
