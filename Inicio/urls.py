from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html',authentication_form = CustomAuthenticationForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'),name='logout'),
    path('inicio/',login_required(TemplateView.as_view(template_name='inicio.html')),name='inicio'),

    # Organismos
    path('inicio/organismos/crear', login_required(OrganismosCreateView.as_view()),name='organismos_crear'), 
    path('inicio/organismos/listar', login_required(OrganismosListView.as_view()),name='organismos_listar'), 
    path('inicio/organismos/ver/<pk>', login_required(OrganismosDetailView.as_view()),name='organismos_ver'), 
    path('inicio/organismos/editar/<pk>', login_required(OrganismosUpdateView.as_view()),name='organismos_editar'), 
    path('inicio/organismos/eliminar/<pk>', login_required(OrganismosDeleteView.as_view()),name='organismos_eliminar'), 

]

