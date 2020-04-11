
var DATA = JSON.parse(document.getElementById('data').textContent);
var DATA_OUT=undefined

console.log(DATA.is_web_cam)


var player = document.getElementById('player');
const constraints = {
    video: {
        facingMode: 'environment'
      },
    audio:false
};

var face_to_register = document.getElementById("face_to_register")
var faces_registered_list = document.getElementById("faces_registered_list")
var face_selection = -1
var face_name_selection = "unknown"

for(var i=1;i<DATA.faces_registered.length;i++)
{

    var listItem = document.createElement("li")
    listItem.className="list-group-item list-group-item-dark"
    listItem.textContent = DATA.faces_registered[i]
    console.log(listItem) 
    listItem.tabIndex="1"
    faces_registered_list.appendChild(listItem)
    
}
//SELECT FACE ON LIST
faces_registered_list.onclick = function (event) {
    var target = event.target
    if (face_selection!=-1)
        faces_registered_list.childNodes[face_selection+1].className="list-group-item list-group-item-dark"
    
    face_selection = $(target).index()
    face_name_selection =faces_registered_list.childNodes[face_selection+1].textContent
    console.log("saf",face_name_selection)
    faces_registered_list.childNodes[face_selection+1].className="list-group-item active"
    DATA_OUT_AUX={
        'face_name': face_name_selection
    }
    $.getJSON(DATA.URL_GET_FACES_IMAGES, DATA_OUT_AUX)
        .done(function (response) {
            var counter_imgs=0
            for(var i=0;i<response.images.length;i++){


                //console.log(response.images[i])
                var img = new Image();   // Create new img element
                img.onload = function() {       
                    if(counter_imgs==0)     
                        context.drawImage(this, 0, 0, canvas.width, canvas.height);                         
                    else if(counter_imgs==1)
                        context1.drawImage(this, 0, 0, canvas1.width, canvas1.height);     
                    else if(counter_imgs==2)
                        context2.drawImage(this, 0, 0, canvas2.width, canvas2.height);     
                    else if(counter_imgs==3)
                        context3.drawImage(this, 0, 0, canvas3.width, canvas3.height);
                    counter_imgs=counter_imgs+1
                
                };
                img.src =response.images[i]
            }
    })
    .fail(function (response, textStatus, error) {
        console.log(response, textStatus, error)
    })
}

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
/// BUTTONS ZONE    
    var train_button = document.getElementById("train_button")
    train_button.onclick=function(ev){
        $.getJSON(DATA.URL_UPDATE_FACE_MODEL, {"none":"none"})
            .done(function (response) {
            console.log(response)
            faces_registered_list.removeChild(item_selected)
        })
        .fail(function (response, textStatus, error) {
            console.log(response, textStatus, error)
        })
    }
    var delete_face_button = document.getElementById("delete_face_button")
    delete_face_button.onclick=function(ev){
        if(face_selection!=-1)
        {   
            item_selected=faces_registered_list.childNodes[face_selection+1]
            DATA_OUT_AUX={
                'face_name':item_selected.textContent
            }
            
            $.getJSON(DATA.URL_DELETE_FACES_IMAGES, DATA_OUT_AUX)
                .done(function (response) {
                console.log(response)
                faces_registered_list.removeChild(item_selected)
            })
            .fail(function (response, textStatus, error) {
                console.log(response, textStatus, error)
            })
        }
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
            face_to_register.disabled=false
            counter_context=counter_context+1
            this.innerHTML="clear images"
        }else{
            counter_context=0
            context.clearRect(0, 0, canvas.width, canvas.height);
            context1.clearRect(0, 0, canvas1.width, canvas1.height);
            context2.clearRect(0, 0, canvas2.width, canvas2.height);
            context3.clearRect(0, 0, canvas3.width, canvas3.height);

            face_to_register.disabled=true
            this.innerHTML="capture image"
            return;
        }
        //SEND IMAGE AND SAVE WITH NAME
    }

    var register_button = document.getElementById("register_button")
    register_button.onclick=function(ev){
        console.log(counter_context)
        if(counter_context==4){
            console.log("REGISTER FACE: ", face_to_register.value)

            DATA_OUT_AUX={
                'images':'s',
                'face_name':face_to_register.value
            }
            DATA_OUT_AUX.images=[
                canvas.toDataURL(image_format),
                canvas1.toDataURL(image_format),
                canvas2.toDataURL(image_format),
                canvas3.toDataURL(image_format)
            ]
            console.log("fetching..",DATA_OUT_AUX)
            
            $.post(DATA.URL_ADD_NEW_FACE, DATA_OUT_AUX)
            .done(function (response) {
                console.log("response", response)
               
            })
            .fail(function (response, textStatus, error) {
                console.log(response, textStatus, error)
            })



            var listItem = document.createElement("li")
            listItem.className="list-group-item list-group-item-dark"
            listItem.textContent = face_to_register.value
            console.log(listItem) 
            listItem.tabIndex="1"
            faces_registered_list.appendChild(listItem)
        }
    }
    //MANAGE VISIBILITY 
    container_ip_cam.hidden=true
    container_web_cam.hidden=false


    navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
        player.srcObject = stream;
     
    })
    .catch(function(err){
        console.log(err)
    });

    if(selected_task.value=="register"){
        register_button.hidden=false
        detection_containter.hidden=true
        register_containter.hidden=false
        capture_button.disabled=false
        if(counter_context==4){
            face_to_register.disabled=false
        }
        clearInterval(schedule_task)
    }else if(selected_task.value=="detect"){
        schedule_task = setInterval(fetchZones, 5000);

        register_button.hidden=true
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
            if(counter_context==3){
                face_to_register.disabled=false

            }
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