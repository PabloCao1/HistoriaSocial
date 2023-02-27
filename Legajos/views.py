from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy


#region ############################################################### Legajos

class LegajosListView(ListView):    
    model = Legajos

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | 
                Q(apellido__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list
   
class LegajosDetailView(DetailView):   
    model = Legajos

class LegajosDeleteView(DeleteView):    
    model = Legajos
    success_url= reverse_lazy("Legajos_listar")

class LegajosCreateView(CreateView):    
    model = Legajos
    form_class = LegajosForm    

class LegajosUpdateView(UpdateView):
    model = Legajos
    form_class = LegajosForm    
#endregion
