let DATA = JSON.parse(document.getElementById('data').textContent);

//IS THE REAL TIME CAMERA, IF IS POSSIBLE TO USE, IS USSEFULL TO TAKE PICTURE FASTER.
//OR MAKE DETECTIONS IN "REAL TIME"
let player_container = document.getElementById("player_container")
let player = document.getElementById('player');



//CONTAINERS SELECTED DEPENDING IF CAMERA IS IP OR NOT.
let container_ip_cam = document.getElementById("container_ip_cam")
let container_web_cam = document.getElementById("container_web_cam")


//CONTAINERS SELECTED WITH select_task.js
let register_containter = document.getElementById("register_containter")
let detection_containter = document.getElementById("detection_containter")


//CANVAS USING TO SAVE, AND SHOW THE IMAGE CAPTURED AND REGESITERED FACES
let image = document.getElementById("img")
let canvas = document.getElementById("myCanvas")
let canvas1 = document.getElementById("myCanvas1")
let canvas2 = document.getElementById("myCanvas2")
let canvas3 = document.getElementById("myCanvas3")

const context = canvas.getContext('2d');
const context1 = canvas1.getContext('2d');
const context2 = canvas2.getContext('2d');
const context3 = canvas3.getContext('2d');


//DETECTION CANVAS  TO SHOW, DETECTION CANVAS AUX TO PROCCESS.
let detection_canvas = document.getElementById("detection_canvas")
let detection_canvas_aux = document.getElementById("detection_canvas_aux")
const detection_context = detection_canvas.getContext('2d');
const detection_context_aux = detection_canvas_aux.getContext('2d');

let counter_context = 0
let image_format = "image/png"
let schedule_task = false


document.writeln("<script type='text/javascript' src='../static/js/face_recognition/utils/face_registered_list.js'></script>");
document.writeln("<script type='text/javascript' src='../static/js/face_recognition/utils/main_buttons.js'></script>");


if (DATA.is_web_cam) {


    //ASK IF IS A MOBILE LOADING THE PAGE, IF IT IS LOAD PLAYERMOBILE VERSION.
    document.writeln("<script type='text/javascript' src='../static/js/face_recognition/web_cam/utils/is_cellphone.js'></script>");
    document.writeln("<script type='text/javascript' src='../static/js/face_recognition/web_cam/web_cam.js'></script>");

} else {
   

    document.writeln("<script type='text/javascript' src='../static/js/face_recognition/ip_camera/ip_camera.js'></script>");


}


document.writeln("<script type='text/javascript' src='../static/js/face_recognition/utils/select_task.js'></script>");


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