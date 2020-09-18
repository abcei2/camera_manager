from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from core.view_utils import BaseView
from core.models import User
from cameras.models import Camera


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
def delete_camera(request):
    if request.method == 'GET':
        id_cam = request.GET.get('id_cam')
        Camera.objects.get(pk=id_cam).delete()
        return render(request, 'cam/cam_list.html', {'data': 'data'})


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
def create_new_camera(request):
    web_cam = request.GET.get('web_cam')
    url = request.GET.get('url')
    geopoint = request.GET.get('geopoint')
    detector_type = request.GET.get('detector_type')
    user_id = request.GET.get('user_id')

    
    user = User.objects.get(id=user_id)
    new_cam = Camera(url=url, geopoint=geopoint,
                     detector_type=detector_type, web_cam=web_cam,user=user)
    new_cam.save()

    CAM_DATA = {
        'url': url,
        'geopoint': geopoint
    }
    return JsonResponse(CAM_DATA, safe=False)


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
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


@login_required(login_url=settings.LOGOUT_REDIRECT_URL,
redirect_field_name=settings.LOGOUT_REDIRECT_URL)
def get_camera_position(request):
    all_cams = []

    cameras_all = Camera.objects.filter(is_active=True)
    for cam in cameras_all:
        cameras = {
            'shortid': cam.short_id,
            'id_cam': cam.id,
            'coords': cam.coords,
            'detector_type': cam.detector_type,
        }
        all_cams.append(cameras)
    return JsonResponse({'cameras': all_cams}, safe=False)


class CamListView(LoginRequiredMixin, ListView):
    model = Camera
    template_name = 'cam/cam_list.html'

    login_url = settings.LOGOUT_REDIRECT_URL
    redirect_field_name = settings.LOGOUT_REDIRECT_URL
    


class CamCreateView(LoginRequiredMixin, BaseView):
    template = 'cam/cam_add.html'

    login_url = settings.LOGOUT_REDIRECT_URL
    redirect_field_name = settings.LOGOUT_REDIRECT_URL
    def get(self, request):
        return self.render_template(request, {'data': {
            "MAP_API": settings.MAP_API,
            "URL_SUMMIT": reverse('cameras:create_new_camera'),
            "URL_REDIRECT": reverse('cameras:manage_cameras')
        }})
