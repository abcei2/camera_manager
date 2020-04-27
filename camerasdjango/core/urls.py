from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

from core.views import home


urlpatterns = [
    path('', home, name='home'),
    path('cameras/', include(
        ('cameras.urls', 'cameras'), namespace='cameras')),
    path(
        'face_recognition/',
        include(
            ('face_recognition.urls', 'face_recognition'),
            namespace='face_recognition'
        )
    ),
    path('admin/', admin.site.urls),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
