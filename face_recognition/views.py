import cv2
import json
import time
import mrcnn
import numpy as np

from django.db import connection
from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from typing import Dict, Any
from decimal import Decimal
# UTILS FUNCTIONS
from core.utils import coords_in_radius
# ALL MODELS
from face_recognition.models import FaceRecognitionCamera_reports
from face_recognition.models import FaceRecognitionCamera
from cameras.models import Camera
# IMAGE TO STRING
from django.core.serializers import serialize
import base64
# CHARTS
from datetime import datetime, timedelta
from random import seed
from random import random
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

import requests

def manage_detection(request, id_cam):

    detection_zone = FaceRecognitionCamera.objects.filter(camera_id__exact=id_cam)
    camera = Camera.objects.filter(pk=id_cam)
    detection_zone_json = json.loads(serialize('json', detection_zone))[0]
    camera_json = json.loads(serialize('json', camera))[0]

    data = {
        'data': {
            'id_cam':id_cam,
            'url':camera_json['fields']['url'], 
            'URL_EDIT': reverse('cameras:edit_url_camera'),
            'URL_GET_DETECTIONS': reverse('face_recognition:get_detection'),
            'is_web_cam':camera_json['fields']['web_cam']
        }
    }
    print(data) 
    return render(request, 'face_recognition/manage_detection.html', data)

global bussy
bussy=False
@csrf_exempt
def get_detection(request):
    global bussy
    if bussy:
        DATA = {
            'message': "is bussy"
        }
        print("bussy")
        return JsonResponse(DATA, safe=False)

    bussy=True
    
    img = request.POST.get('img')
    format, imgstr = img.split(';base64,') 
    ext = format.split('/')[-1] 
    imgstr=base64.b64decode(imgstr)
    with open(f'static/temp.{ext}', 'wb') as file1:
        file1.write(imgstr)
    frame=cv2.imread(f'static/temp.{ext}')
    frame_not_draw=frame.copy()
    frame_to_upload=cv2.imencode(".png", frame)[1]

    ##### DETECT FACES AND LANDMARKS
    files = {'file': ('image.jpg', frame_to_upload, 'multipart/form-data')}

    response = requests.post(f'https://ai.tucanoar.com/faces/detect_faces/',
                                files=files)
    detections=response.json()
    for faces in detections['message']['faces_detected']:

        ##### DRAW BBOX AND LANDMARKS
        cv2.rectangle(frame,(faces['upper_left'][0],faces['upper_left'][1]),(faces['down_right'][0],faces['down_right'][1]),(0,200,0))
        for landmark in faces["landmarks"]:
            cv2.circle(frame, (landmark[0],landmark[1]),  2, (0, 255, 0), -1) 

        face_image=frame_not_draw[faces['upper_left'][1]:faces['down_right'][1],faces['upper_left'][0]:faces['down_right'][0]]
        
        
        face_image_to_upload=cv2.imencode(".jpg", face_image)[1]

        ##### CLASSIFY FACES
        files = {'file': ('image.jpg', face_image_to_upload, 'multipart/form-data')}

        response = requests.post(f'https://ai.tucanoar.com/faces_classify/classify_faces/',
                                files=files)
        classifications=response.json()

        cv2.putText(frame, classifications['message']['face_detect'], (faces['upper_left'][0],faces['upper_left'][1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.imwrite("static/detection_output.png",frame)

    with open(f'static/detection_output.png', 'rb') as file1:

        my_string = base64.b64encode(file1.read())
        my_string="data:image/png;base64,"+str(my_string)[2:-1]
        print()
        DATA = {
            'img':str(my_string)
        }
    bussy=False
    return JsonResponse(DATA, safe=False)

    
class BaseView(View):
    def global_context(self, request=None):
        return {
            'DEBUG': settings.DEBUG,
            'view': f'{self.__module__}.{self.__class__.__name__}',
            'sql_queries': len(connection.queries),
        }

    def render_template(self, request, context=None, template=None):
        return render(request, template or self.template, {
            **self.global_context(),
            **(context or {}),
        })

    def render_json(self, json_dict: Dict[str, Any], **kwargs):
        return JsonResponse(json_dict, **kwargs)


def get_reports(request):
    result = []
    face_reports = FaceRecognitionCamera_reports.objects.filter(
        camera_id__exact=cam.id)[0]

    face_reports = json.loads(serialize('json', face_reports))[0]
    print(face_reports)

    result.append({'name': 'name', "data": 'data'})
    return result



# CHARTS


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


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()


def dashboard(request, id_cam):

   
    context = {"categories": categories, 'values': values}
    print(context)
    return render(request, 'face_recognition/dashboard.html', context=context)
