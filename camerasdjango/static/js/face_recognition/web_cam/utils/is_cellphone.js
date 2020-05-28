
let is_mobile = false
let player_mobile = document.getElementById("player_mobile")



if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {

     
    function _arrayBufferToBase64(buffer) {
        var binary = ''
        var bytes = new Uint8Array(buffer)
        var len = bytes.byteLength;
        for (var i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i])
        }
        return window.btoa(binary);
    }
    var rotation = {
        1: 0,
        3: 180,
        6: 90,
        8: 270
    };
    
    is_mobile = true

    player_container.hidden = true
    capture_button.hidden = true
    player_mobile.hidden = false

    let counter_imgs = 0
    function orientation(file, callback) {

        var fileReader = new FileReader();
        fileReader.onloadend = function() {
            var base64img = "data:" + file.type + ";base64," + _arrayBufferToBase64(fileReader.result);
            var scanner = new DataView(fileReader.result);
            var idx = 0;
            var value = 1; // Non-rotated is the default
            if (fileReader.result.length < 2 || scanner.getUint16(idx) != 0xFFD8) {
            // Not a JPEG
            if (callback) {
                callback(base64img, value);
            }
            return;
            }
            idx += 2;
            var maxBytes = scanner.byteLength;
            while (idx < maxBytes - 2) {
            var uint16 = scanner.getUint16(idx);
            idx += 2;
            switch (uint16) {
                case 0xFFE1: // Start of EXIF
                var exifLength = scanner.getUint16(idx);
                maxBytes = exifLength - idx;
                idx += 2;
                break;
                case 0x0112: // Orientation tag
                // Read the value, its 6 bytes further out
                // See page 102 at the following URL
                // http://www.kodak.com/global/plugins/acrobat/en/service/digCam/exifStandard2.pdf
                value = scanner.getUint16(idx + 6, false);
                maxBytes = 0; // Stop scanning
                break;
            }
            }
            if (callback) {
            callback(base64img, value);
            }
        }
        fileReader.readAsArrayBuffer(file);
    };

    player_mobile.addEventListener('change', function(e) {

        let file = e.target.files[0];
        
        if (file) {

            orientation(file, function(base64img, value) {

                // Do something with the video file.
                let img = new Image()
                //img.src = base64img;
                img.src = URL.createObjectURL(file);
                img.onload = function() {
                    let width1=0
                    let height1=0
                    if(this.width>this.height){
                        width1 = 600;
                        height1 = width1 * (img.height / img.width)
                    } else {
                        height1 = 600;
                        width1 = height1  * ( this.width/this.height);
                    }   
                    if (selected_task.value == "register") {
                        if (counter_context == 0) {
                            canvas.width=width1
                            canvas.height=height1
                            context.drawImage(this, 0, 0, canvas.width, canvas.height)
                            counter_context = counter_context + 1
                            image = canvas.toDataURL(image_format)
                        } else if (counter_context == 1) {
                            canvas1.width=width1
                            canvas1.height=height1
                            context1.drawImage(this, 0, 0, canvas1.width, canvas1.height)
                            counter_context = counter_context + 1
                            image = canvas1.toDataURL(image_format)
                        } else if (counter_context == 2) {
                            canvas2.width=width1
                            canvas2.height=height1
                            context2.drawImage(this, 0, 0, canvas2.width, canvas2.height)
                            counter_context = counter_context + 1
                            image = canvas2.toDataURL(image_format)
                        } else if (counter_context == 3) {
                            canvas3.width=width1
                            canvas3.height=height1
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

                        detection_canvas_aux.width=width1
                        detection_canvas_aux.height=height1

                        detection_canvas.width=width1
                        detection_canvas.height=height1
                        detection_context_aux.drawImage(this, 0, 0, detection_canvas_aux.width, detection_canvas_aux.height);
                        
                        image = detection_canvas_aux.toDataURL(image_format);
                        
                        $.post(DATA.URL_GET_DETECTIONS, {
                                id_cam:DATA.id_cam,
                                img: image,
                                rotate_angle:rotation[value]
                            })
                            .done(function(response) {
                                let img2 = new Image()
                                img2.src = response.img
                                img2.onload = () => detection_context.drawImage(
                                    img2, 0, 0, detection_canvas.width, detection_canvas.height)

                            })
                            .fail((response, textStatus, error) => {
                                console.log(response, textStatus, error)
                            })
                    }

                };

            });
        }
        
    });

} else {
    player_container.hidden = false
    player_mobile.hidden = true
    capture_button.hidden = false
}


