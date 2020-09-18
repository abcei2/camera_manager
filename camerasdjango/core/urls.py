from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

from core.views import login_user


urlpatterns = [
    # accounts/admin
    path('login/', login_user, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    # apps
    path('api/', include(('api_manager.urls', 'api_manager'), namespace='api')),
    path('cameras/', include(
        ('cameras.urls', 'cameras'), namespace='cameras')),
    path(
        'face_recognition/',
        include(
            ('face_recognition.urls', 'face_recognition'),
            namespace='face_recognition'
        )
    ),

    # other
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
