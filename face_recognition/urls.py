from django.urls import path
from django.conf.urls import url

from face_recognition.views import (
   manage_detection, get_reports, LineChartJSONView, TemplateView,dashboard, get_detection
)


line_chart = TemplateView.as_view(template_name='face_recognizer/manage_detection.html')
line_chart_json = LineChartJSONView.as_view()

app_name = 'face_recognition'
urlpatterns = [
    path('<str:id_cam>/manage_detection/', manage_detection, name='manage_detection'),  
    path('<str:id_cam>/dashboard/', dashboard, name='dashboard'), 

    path('line_chart_json/', line_chart_json, name='line_chart_json'),
    path('get_detection/', get_detection, {}, name='get_detection'),
    path('get_reports/', get_reports, {}, name='get_reports'),
  #  url(r'^manage_cameras/manage_spots/$', manage_spots, name='manage_spots'),    
]