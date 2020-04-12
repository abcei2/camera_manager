from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.urls import reverse

from core.view_utils import BaseView
from cameras.models import Camera
from face_recognition.models import FaceRecognitionCamera


def delete_camera(request):
    if request.method == 'GET':
        id_cam = request.GET.get('id_cam')
        print(id_cam)
        camera_of_spots = Camera.objects.get(pk=id_cam)
        camera_of_spots.delete()
        return render(request, 'cam/cam_list.html', {'data': 'data'})


def create_new_camera(request):
    web_cam = request.GET.get('web_cam')
    url = request.GET.get('url')
    geopoint = request.GET.get('geopoint')
    model_detector = request.GET.get('model_detector')
    new_cam = Camera(url=url, geopoint=geopoint,
                     model_detector=model_detector, web_cam=web_cam)
    new_cam.save()

    if(model_detector == 'FR'):
        FaceAux = FaceRecognitionCamera(camera=new_cam)
        FaceAux.save()

    CAM_DATA = {
        'url': url,
        'geopoint': geopoint
    }
    return JsonResponse(CAM_DATA, safe=False)


def edit_url_camera(request):
    url = request.GET.get('url')
    id_cam = request.GET.get('id_cam')
    CAM_DATA = {
        'url': url
    }
    try:
        camera_of_spots = Camera.objects.get(pk=id_cam)
    except (KeyError, Camera.DoesNotExist):
        CAM_DATA.url = "BAAD"
        return JsonResponse(CAM_DATA, safe=False)
    else:
        camera_of_spots.url = url
        camera_of_spots.save()
    return JsonResponse(CAM_DATA, safe=False)


def get_camera_position(request):
    all_cams = []

    cameras_all = Camera.objects.filter(is_active=True)
    for cam in cameras_all:
        cameras = {
            'shortid': cam.short_id,
            'id_cam': cam.id,
            'coords': cam.coords,
            'model_detector': cam.model_detector,
        }
        all_cams.append(cameras)
    return JsonResponse({'cameras': all_cams}, safe=False)


class CamListView(ListView):
    model = Camera
    template_name = 'cam/cam_list.html'


class CamCreateView(BaseView):
    template = 'cam/cam_add.html'

    def get(self, request):
        return self.render_template(request, {'data': {
            "MAP_API": settings.MAP_API,
            "URL_SUMMIT": reverse('cameras:create_new_camera'),
            "URL_REDIRECT": reverse('cameras:manage_cameras')
        }})
