//MANAGE VISIBILITY


if (selected_task.value == "register") {
    register_button.hidden = false
    detection_containter.hidden = true
    register_containter.hidden = false
    capture_button.innerHTML="Capture"
    if (counter_context == 4) {
        face_to_register.disabled = false
    }
    schedule_task = false
} else if (selected_task.value == "detect") {
  
    register_button.hidden = true
    detection_containter.hidden = false
    register_containter.hidden = true
    capture_button.innerHTML="Detect"
    face_to_register.disabled = true
}

selected_task.addEventListener('change', function(ev) {
    if (this.value == "register") {
        detection_containter.hidden = true
        register_containter.hidden = false
        capture_button.innerHTML="Capture"
        if (counter_context == 3) {
            face_to_register.disabled = false
        }
        schedule_task = false
    } else if (this.value == "detect") {
        detection_containter.hidden = false
        register_containter.hidden = true
        capture_button.innerHTML="Detect"
        face_to_register.disabled = true
    }
})
