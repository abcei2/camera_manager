

var DATA = JSON.parse(document.getElementById('data').textContent);
var DATA_OUT=undefined

console.log(DATA.is_web_cam)


var player = document.getElementById('player');
const constraints = {
    video: true,
};
var container_ip_cam = document.getElementById("container_ip_cam")
var container_web_cam = document.getElementById("container_web_cam")

var image = document.getElementById("img")
var canvas = document.getElementById("myCanvas")
var canvas1 = document.getElementById("myCanvas1")
var canvas2 = document.getElementById("myCanvas2")
var canvas3 = document.getElementById("myCanvas3")



var selected_task = document.getElementById("selected_task")

var detection_canvas = document.getElementById("detection_canvas")
var detection_canvas_aux= document.getElementById("detection_canvas_aux")

var register_containter = document.getElementById("register_containter")
var detection_containter = document.getElementById("detection_containter")
var face_to_register = document.getElementById("face_to_register")

const context = canvas.getContext('2d');
const context1 = canvas1.getContext('2d');
const context2 = canvas2.getContext('2d');
const context3 = canvas3.getContext('2d');
const detection_context = detection_canvas.getContext('2d');
const detection_context_aux = detection_canvas_aux.getContext('2d');

var counter_context=0
var image_format="image/png"
var schedule_task = undefined
function fetchZones(){
    detection_context_aux.drawImage(player, 0, 0, detection_canvas_aux.width, detection_canvas_aux.height);
    
    image = detection_canvas_aux.toDataURL(image_format);
    DATA_OUT.img=image
    console.log("fetching..",DATA_OUT)
    
    $.post(DATA.URL_GET_DETECTIONS, DATA_OUT)
    .done(function (response) {
        console.log("response", response.img)
        var img = new Image();   // Create new img element
        img.onload = function() { 
            detection_context.drawImage(img, 0, 0, detection_canvas.width, detection_canvas.height);
        
        };
        img.src =response.img
       
    })
    .fail(function (response, textStatus, error) {
        console.log(response, textStatus, error)
    })
}
if(DATA.is_web_cam){

    DATA_OUT={
        'img':'empty'
    }
    
    var capture_button = document.getElementById("capture_button")
    capture_button.onclick=function(ev){
        if(counter_context==0){
            context.drawImage(player, 0, 0, canvas.width, canvas.height);
            counter_context=counter_context+1
            image = canvas.toDataURL(image_format);
        }
        else if(counter_context==1){
            context1.drawImage(player, 0, 0, canvas1.width, canvas1.height);
            counter_context=counter_context+1
            image = canvas1.toDataURL(image_format);
        }else if(counter_context==2){
            context2.drawImage(player, 0, 0, canvas2.width, canvas2.height);
            counter_context=counter_context+1
            image = canvas2.toDataURL(image_format);
        }else if(counter_context==3){
            context3.drawImage(player, 0, 0, canvas3.width, canvas3.height);
            image = canvas3.toDataURL(image_format);
            counter_context=counter_context+1
        }else
            counter_context=0
    }
    //MANAGE VISIBILITY 
    container_ip_cam.hidden=true
    container_web_cam.hidden=false


    navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
        player.srcObject = stream;
     
    });

    if(selected_task.value=="register"){
        detection_containter.hidden=true
        register_containter.hidden=false
        capture_button.disabled=false
        face_to_register.disabled=false
        clearInterval(schedule_task)
    }else if(selected_task.value=="detect"){
        schedule_task = setInterval(fetchZones, 5000);
        detection_containter.hidden=false
        register_containter.hidden=true
        capture_button.disabled=true
        face_to_register.disabled=true
    }
    
    selected_task.onchange=function(ev){
        console.log(this.value)
        if(this.value=="register"){
            detection_containter.hidden=true
            register_containter.hidden=false
            capture_button.disabled=false
            face_to_register.disabled=false
            clearInterval(schedule_task)
        }else if(this.value=="detect"){
            schedule_task = setInterval(fetchZones, 5000);
            detection_containter.hidden=false
            register_containter.hidden=true
            capture_button.disabled=true
            face_to_register.disabled=true
        }
    }

   

    
}else{
    var toggle_url=false
    var edit_url_button = document.getElementById("edit_url_button")
    var url_cam = document.getElementById("url_cam")
    container_ip_cam.hidden=false
    container_web_cam.hidden=true   

    url_cam.value=DATA.url
    
    edit_url_button.onclick=function(){


        if(toggle_url){
            edit_url_button.innerHTML="Edit url"
            DATA.url=url_cam.value
            image.src=url_cam.value
    
            toggle_url=false
            url_cam.disabled=true
    
    
            $.getJSON(DATA.URL_EDIT, DATA)
            .done(function (response) {
                console.log("response", response)
            })
            .fail(function (response, textStatus, error) {
                console.log(response, textStatus, error)
            })
        }else{
            edit_url_button.innerHTML="Save url"
            toggle_url=true
            url_cam.disabled=false
        }
}

}