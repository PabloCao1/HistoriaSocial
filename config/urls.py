from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [

    # path('hsu_admin/', admin.site.urls),    # TODO crear un honey_pot para controlar intrusiones
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),    
    path('', include('Inicio.urls')),
    path('', include('Legajos.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)