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