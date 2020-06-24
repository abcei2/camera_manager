from django.urls import path

from face_recognition.views import (
    manage_detection, get_reports, dashboard,
    get_detection, add_new_face, get_face_by_name, delete_face_by_name,
    update_faces_model
)


app_name = 'face_recognition'
urlpatterns = [
    path('<str:id_cam>', manage_detection, name='manage_detection'),
    path('<str:id_cam>/dashboard/', dashboard, name='dashboard'),


    path('get_detection/', get_detection, {}, name='get_detection'),
    path('get_face_by_name/', get_face_by_name, {}, name='get_face_by_name'),
    path('add_new_face/', add_new_face, {}, name='add_new_face'),
    path('get_reports/', get_reports, {}, name='get_reports'),

    path('update_faces_model/', update_faces_model,
         {}, name='update_faces_model'),

    path('delete_face_by_name/', delete_face_by_name,
         {}, name='delete_face_by_name'),

]
