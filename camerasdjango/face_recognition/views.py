import os
import cv2
import json
import base64
import shutil
import requests

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect

from django.utils.translation import ugettext_lazy as _

from chartjs.views.lines import BaseLineChartView

from core.utils import frame_from_b64image
from face_recognition.models import FaceRecognitionReport, Face
from cameras.models import Camera
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


register_face_service_url="https://ai.tucanoar.com/faces_classify/delete_images/"
update_model_service_url="https://ai.tucanoar.com/faces_classify/update_model/"
delete_images_service_url="https://ai.tucanoar.com/faces_classify/delete_images/"
detect_faces_service_url="https://ai.tucanoar.com/faces/detect_faces/"
classify_faces_service_url="https://ai.tucanoar.com/faces_classify/classify_faces/"

# global detecting, counter_tabs
# counter_tabs=0
# detecting=False
@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_GET
def manage_detection(request, id_cam):
    
    # if request.session.get('bussy', False):
    #     request.session["bussy"].append(request.user.id)
    #     request.session["bussy2"].append(counter_tabs)
    #     print(request.session.get('bussy', False))
    #     print(request.session.get('bussy2', False))
    # else:
    #     request.session["bussy"]=[request.user.id]
    #     request.session["bussy2"]=[counter_tabs]
        
    faces = Face.objects.values_list('name', flat=True)
    camera = Camera.objects.get(id=id_cam)

    context = {
        'data': {
            'url': camera.url,
            'is_web_cam': camera.web_cam,
            'faces_registered': list(faces),

            'URL_FREE_DETECTOR':reverse('face_recognition:free_detector'),
            'URL_EDIT': reverse('cameras:edit_url_camera'),
            'URL_GET_DETECTIONS': reverse('face_recognition:get_detection'),
            'URL_ADD_NEW_FACE': reverse('face_recognition:add_new_face'),
            'URL_GET_FACES_IMAGES': reverse(
                'face_recognition:get_face_by_name'),
            'URL_DELETE_FACES_IMAGES': reverse(
                'face_recognition:delete_face_by_name'),
            'URL_UPDATE_FACE_MODEL': reverse(
                'face_recognition:update_faces_model'),
        },
        'SITE_TITLE': "Tucano AI"
    }
    return render(request, 'face_recognition/manage_detection.html', context)


@csrf_protect
@require_POST
def free_detector(request):
    print("FREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

    return JsonResponse({'message': _("Done")})

@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_GET
def update_faces_model(request):
    requests.get(delete_images_service_url)

    folder_url = settings.FACES_DIR
    face_names_list = os.listdir(folder_url)
    for face_name in face_names_list:
        face_image_list = os.listdir(f'{folder_url}/{face_name}')
        for face_image in face_image_list:
            face_frame = cv2.imread(f'{folder_url}/{face_name}/{face_image}')

            files = {
                'json': (
                    None,
                    json.dumps({"face_name": face_name}),
                    'application/json'
                ),
                'file': (
                    'image.jpg',
                    cv2.imencode(".png", face_frame)[1],
                    'multipart/form-data'
                )
            }
            requests.post(
                register_face_service_url,
                files=files
            )
        
        print(files)

    requests.get(update_model_service_url)
    print("UPDATING FACE MODEL")
    return JsonResponse({'message': _("Done")})


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_GET
def delete_face_by_name(request):
    face_name = request.GET.get('face_name')
    Face.objects.filter(name=face_name).delete()

    try:
        shutil.rmtree(f'{settings.FACES_DIR}/{face_name}')
    except FileNotFoundError:
        pass

    return JsonResponse({'message': _("Face deleted")}, safe=False)


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_GET
def get_face_by_name(request):
    face_name = request.GET.get('face_name')

    images = []
    faces_path = f'{settings.FACES_DIR}/{face_name}'

    try:
        for face_file in os.listdir(faces_path):
            with open(f'{faces_path}/{face_file}', 'rb') as fp:
                my_string = base64.b64encode(fp.read())
                my_string = "data:image/png;base64, " + str(my_string)[2:-1]
                images.append(my_string)
    except FileNotFoundError:
        pass

    return JsonResponse({'images': images}, safe=False)


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_POST
def add_new_face(request):
    face_name = request.POST.get('face_name')
    images = request.POST.getlist('images[]', [])

    faces_dir = f"{settings.FACES_DIR}/{face_name}"
    if not os.path.isdir(faces_dir):
        os.mkdir(faces_dir)

    for counter_img, img in enumerate(images):
        frame = frame_from_b64image(img.split(';base64,')[1])

        image_to_upload = cv2.imencode(".png", frame)[1]

        response = requests.post(
            detect_faces_service_url,
            files={
                'file': ('image.jpg', image_to_upload, 'multipart/form-data')
            }
        )
        detections = response.json()

        if detections['message']['num_of_detections'] != 1:
            return JsonResponse(
                {'message': _("Couldn't detect exactly one face")},
                status=503
            )

        face = detections['message']['faces_detected'][0]
        face_image = frame[
            face['upper_left'][1]:face['down_right'][1],
            face['upper_left'][0]:face['down_right'][0]
        ]

        cv2.imwrite(f"{faces_dir}/{counter_img}.png", face_image)

    Face.objects.create(name=face_name)

    return JsonResponse({'message': _("Face registered")})


bussy = False


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_POST
def get_detection(request):
    
    
    
    
    global bussy



    if bussy:
        return JsonResponse({'message': _("Detector busy")}, status=503)
    

    bussy = True

    img = request.POST.get('img')

    frame = frame_from_b64image(img.split(';base64,')[1])
    frame_not_draw = frame.copy()
    frame_to_upload = cv2.imencode(".png", frame)[1]

    response = requests.post(
        detect_faces_service_url,
        files={'file': ('image.jpg', frame_to_upload, 'multipart/form-data')}
    )

    if response.status_code not in [200, 201]:
        bussy = False
        return JsonResponse(
            {'message': _("Couldn't extract face from image")},
            status=503
        )

    detections = response.json()

    if detections['message']['num_of_detections'] != 1:
        bussy = False
        return JsonResponse(
            {'message': _("Couldn't detect exactly one face")},
            status=503
        )

    face = detections['message']['faces_detected'][0]

    cv2.rectangle(
        frame,
        (face['upper_left'][0], face['upper_left'][1]),
        (face['down_right'][0], face['down_right'][1]),
        (0, 200, 0)
    )

    face_image = frame_not_draw[
        face['upper_left'][1]:face['down_right'][1],
        face['upper_left'][0]:face['down_right'][0]
    ]

    if face_image.size != 0:
        face_to_classify = cv2.imencode(".jpg", face_image)[1]

    response = requests.post(
        classify_faces_service_url,
        files={
            'file': ('image.jpg', face_to_classify, 'multipart/form-data')
        }
    )

    if response.status_code not in [200, 201]:
        bussy = False
        return JsonResponse(
            {'message': _("Failed to classify face :C")},
            status=503
        )

    classifications = response.json()

    cv2.putText(
        frame,
        classifications['message']['face_detect'],
        (face['upper_left'][0], face['upper_left'][1]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
    )

    the_png = cv2.imencode('.png', frame)[1]
    png_as_text = base64.b64encode(the_png).decode("utf-8")

    bussy = False
    return JsonResponse({'img': f"data:image/png;base64, {png_as_text}"})


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
@require_GET
def get_reports(request):
    ask_if_user_login(request)
    face_reports = FaceRecognitionReport.objects.get(
        camera_id__exact=request.GET.get('cam_id'))

    return face_reports


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


def dashboard(request, id_cam):
    # context = {"categories": categories, 'values': values}
    # print(context)
    return render(request, 'face_recognition/dashboard.html', context={})
