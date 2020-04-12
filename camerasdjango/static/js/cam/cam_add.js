var player = document.getElementById('player');
var web_cam_checkbox = document.getElementById("web_cam_checkbox")

web_cam_checkbox.onclick = function(evt) {
    if (web_cam_checkbox.checked) {
        url_cam.value = 0
        url_cam.disabled = true
    } else {
        url_cam.disabled = false

    }

}

var DATA = JSON.parse(document.getElementById('data').textContent)
var model_type_list = document.getElementById("model_type_list")
var longitude_input = document.getElementById("longitude")
var latitude_input = document.getElementById("latitude")
latitude_input.value = "6.148355"
longitude_input.value = "-75.378672"

var url_cam = document.getElementById("url_cam")
if (web_cam_checkbox.checked) {
    url_cam.value = 0
    url_cam.disabled = true
} else {
    url_cam.disabled = false
}

var dummy_map = document.getElementById("dummy_map")
var dummy_img = document.getElementById("dummy_img")
dummy_img.style.display = "none";

var image = document.getElementById("image")
var toggle = false

var sumbit_button = document.getElementById("sumbit_button")
sumbit_button.onclick = function() {
    CAM_DATA = {}
    if (web_cam_checkbox.checked)
        CAM_DATA.web_cam = 'True'
    else
        CAM_DATA.web_cam = 'False'
    CAM_DATA.url = url_cam.value
    CAM_DATA.detector_type = model_type_list.options[model_type_list.selectedIndex].value;
    CAM_DATA.geopoint = longitude_input.value + ',' + latitude_input.value
    console.log(CAM_DATA)
    $.getJSON(DATA.URL_SUMMIT, CAM_DATA)
        .done(function(response) {
            location.replace(DATA.URL_REDIRECT)
            console.log("response", response)
        })
        .fail(function(response, textStatus, error) {
            console.log(response, textStatus, error)
        })

}

var probe_url_button = document.getElementById("probe_url_button")
probe_url_button.onclick = function() {

    if (toggle) {
        toggle = false
        dummy_map.style.display = "block";
        dummy_img.style.display = "none";
        probe_url_button.innerHTML = "Probe URL"
        web_cam_checkbox.disabled = false
        if (web_cam_checkbox.checked) {
            player.srcObject.getVideoTracks().forEach(track => track.stop());
        }

    } else {

        web_cam_checkbox.disabled = true
        toggle = true

        probe_url_button.innerHTML = "Back to map"
        dummy_map.style.display = "none";
        dummy_img.style.display = "block";

        if (web_cam_checkbox.checked) {
            navigator.mediaDevices.getUserMedia({
                    video: true
                })
                .then((stream) => {
                    player.srcObject = stream;

                });
            player.hidden = false
            image.hidden = true
        } else {

            player.hidden = true
            image.hidden = false
            image.src = url_cam.value
        }

    }
    console.log(dummy_map.style.display)
}
var map_loaded = false
mapboxgl.accessToken = DATA.MAP_API

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-75.378672, 6.148355],
    zoom: 18
})

var marker = new mapboxgl.Marker()
    .setLngLat([-75.378672, 6.148355])
    .addTo(map)

document.addEventListener('DOMContentLoaded', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            map.setCenter([
                position.coords.longitude,
                position.coords.latitude
            ])
        })
    } else {
        alert("Geolocation no disponible")
    }
})


map.on('load', function() {
    map_loaded = true
})
map.on('click', function(e) {
    marker.setLngLat([e.lngLat.lng, e.lngLat.lat]).addTo(map)
    latitude_input.value = e.lngLat.lat.toString()
    longitude_input.value = e.lngLat.lng.toString()
    $.ajax({
        url: "http://192.75.71.26/mjpg/video.mjpg",
        type: "GET",
        success: function(result) {

            console.log(result)
        },
        error: function(error) {
            console.log(error)
        }
    })
})
