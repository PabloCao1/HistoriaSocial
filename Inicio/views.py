import datetime
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView
from .mixins import PermissionsMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy


#region ############################################################### Organismos

class OrganismosListView(PermissionsMixin, ListView):    
    permission_required = 'Inicio.view_organismos' 
    model = Organismos

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | 
                Q(referente__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list
   
class OrganismosDetailView(PermissionsMixin,DetailView):
    permission_required = 'Inicio.view_organismos'    
    model = Organismos

class OrganismosDeleteView(PermissionsMixin,SuccessMessageMixin,DeleteView):   
    permission_required = 'Inicio.delete_organismos' 
    model = Organismos
    success_url= reverse_lazy("organismos_listar")
    success_message = "El registro fue eliminado correctamente"   

class OrganismosCreateView(PermissionsMixin,SuccessMessageMixin,CreateView):    
    permission_required = 'Inicio.add_organismos'
    model = Organismos
    form_class = OrganismosForm
    success_message = "%(nombre)s fue registrado correctamente"    

class OrganismosUpdateView(PermissionsMixin,SuccessMessageMixin,UpdateView):
    permission_required = 'Inicio.change_organismos' 
    model = Organismos
    form_class = OrganismosForm    
    success_message = "%(nombre)s fue editado correctamente"   
#endregion