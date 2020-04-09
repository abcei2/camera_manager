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
from face_recognition.models import FacesModel
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
import os
import shutil
import glob

def manage_detection(request, id_cam):

    detection_zone = FaceRecognitionCamera.objects.filter(camera_id__exact=id_cam)
    faces= FacesModel.objects.all()
    faces_registered=['unknown']
    camera = Camera.objects.filter(pk=id_cam)
    detection_zone_json = json.loads(serialize('json', detection_zone))[0]
    camera_json = json.loads(serialize('json', camera))[0]
    for i in json.loads(serialize('json', faces)):
        faces_registered.append(i['fields']['face'])
    print("\nfaces")
    print(faces_registered)
    print("\n")
    data = {
        'data': {
            'id_cam':id_cam,
            'url':camera_json['fields']['url'], 
            'URL_EDIT': reverse('cameras:edit_url_camera'),
            'URL_GET_DETECTIONS': reverse('face_recognition:get_detection'),
            'URL_ADD_NEW_FACE': reverse('face_recognition:add_new_face'),
            'URL_GET_FACES_IMAGES': reverse('face_recognition:get_face_by_name'),
            'URL_DELETE_FACES_IMAGES': reverse('face_recognition:delete_face_by_name'),
            'URL_UPDATE_FACE_MODEL': reverse('face_recognition:update_faces_model'),
            'is_web_cam':camera_json['fields']['web_cam'],
            'faces_registered':faces_registered
        }
    }
    print(data) 
    return render(request, 'face_recognition/manage_detection.html', data)



def update_faces_model(request):
    response=requests.get('https://ai.tucanoar.com/faces_classify/delete_images/')
    
    folder_url=f'static/face_images/' 
    # face_folders=[x[0] for x in os.walk(folder_url)]
    # print(value)
    face_names_list=os.listdir(folder_url)
    for face_name in face_names_list:
        face_image_list=os.listdir(f'{folder_url}/{face_name}')
        for face_image in face_image_list:
           # print(f'{folder_url}/{face_name}/{face_image}')
            face_frame=cv2.imread(f'{folder_url}/{face_name}/{face_image}')
             
            files = {'json': (None, json.dumps({"face_name":face_name}), 'application/json'),
                'file': ('image.jpg', cv2.imencode(".png", face_frame)[1], 'multipart/form-data')}
            response = requests.post(f'https://ai.tucanoar.com/faces_classify/register_face/',
                                files=files)
            
            print(response)

    response=requests.get('https://ai.tucanoar.com/faces_classify/update_model/')      
    print(response)
    DATA = {
        'message':"done"
    }
    return JsonResponse(DATA, safe=False)

def delete_face_by_name(request):
    face_name = request.GET.get('face_name')
    folder_url=f'static/face_images/{face_name}'  
    shutil.rmtree(folder_url)
    FacesModel.objects.filter(face=face_name).delete()
    DATA = {
        'message':"deleted"
    }

    return JsonResponse(DATA, safe=False)

def get_face_by_name(request):

    face_name = request.GET.get('face_name')
    folder_url=f'static/face_images/{face_name}'  
    images=[]
    for counter_img in range(4):
        print(f'{folder_url}/{face_name}_{counter_img}.png')
        with open(f'{folder_url}/{face_name}_{counter_img}.png', 'rb') as file1:
            my_string = base64.b64encode(file1.read())
            my_string="data:image/png;base64,"+str(my_string)[2:-1]
            images.append(my_string)

    DATA = {
        'images':images
    }

    return JsonResponse(DATA, safe=False)


@csrf_exempt
def add_new_face(request):

    print("HEREE!!")
    face_name = request.POST.get('face_name')
    
    images = request.POST.getlist('images[]', None)
    counter_img=0
    folder_url=f'static/face_images/{face_name}'
    print( os.path.isfile(folder_url))

    try:
        os.mkdir(folder_url)
        ##### DETECT FACES AND LANDMARKS
        
       
    
        for img in images:
            format, imgstr = img.split(';base64,') 
            ext = format.split('/')[-1] 
            imgstr=base64.b64decode(imgstr)
            img_url=f'{folder_url}/{face_name}_{counter_img}.{ext}'
            with open(img_url, 'wb') as file1:
                file1.write(imgstr)
            frame=cv2.imread(img_url)
            image_to_upload=cv2.imencode(".png", frame)[1]
            files = {'file': ('image.jpg', image_to_upload, 'multipart/form-data')}

            response = requests.post(f'https://ai.tucanoar.com/faces/detect_faces/',
                                        files=files)
            detections=response.json()           
                
            for faces in detections['message']['faces_detected']:
                face_image=frame[faces['upper_left'][1]:faces['down_right'][1],faces['upper_left'][0]:faces['down_right'][0]]
                cv2.imwrite(img_url,face_image)
            counter_img+=1
        FacesModel_aux=FacesModel(
             face=face_name)
        FacesModel_aux.save()
    except:
        DATA = {
            'message': "face existss"
        }
        return JsonResponse(DATA, safe=False)
        
    
    DATA = {
        'message': "images saveed"
    }
    return JsonResponse(DATA, safe=False)
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
        
        if face_image.size != 0:
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
