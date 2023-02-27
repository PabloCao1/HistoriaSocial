from django.db import models
from .choices import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save,pre_save,m2m_changed # Produce a signal if there is any database action.



#-------------------------------CONFIGURACIONES GENERALES (se usan en todo el proyecto)--------------------------------------



class Secretarias(models.Model):
    nombre = models.CharField(max_length=40)
    obs = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")

    def __str__(self):
        return (self.nombre)

    class Meta:

        ordering = ['nombre']
        verbose_name = 'Secretaría'
        verbose_name_plural = "Secretarías"

    def get_absolute_url(self):
        return reverse('secretarias_ver', kwargs={'pk': self.pk})
    

class Subsecretarias(models.Model):    
    fk_secretaria = models.ForeignKey(Secretarias, on_delete=models.CASCADE)
    nombre  = models.CharField(max_length=40)    
    activo  = models.BooleanField(default=True)
    obs     = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")

    def __str__(self):
        return (self.nombre)

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Subsecretaría'
        verbose_name_plural = "Subecretarías"

    def get_absolute_url(self):
        return reverse('subsecretarias_ver', kwargs={'pk': self.pk})


class Programas(models.Model):    
    fk_subecretaria = models.ForeignKey(Subsecretarias, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    activo = models.BooleanField(default=True)
    obs = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")

    def __str__(self):
        return (self.nombre)

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa'
        verbose_name_plural = "Programas"

    def get_absolute_url(self):
        return reverse('programas_ver', kwargs={'pk': self.pk})


class Organismos(models.Model):    
    nombre          = models.CharField(max_length=250)
    tipo            = models.CharField(max_length=50, choices=CHOICE_TIPO_ORGANIZACION)
    calle           = models.CharField(max_length=250, null=True, blank=True)
    altura          = models.IntegerField(null=True, blank=True)
    piso            = models.CharField(max_length=100, null=True, blank=True)
    barrio          = models.CharField(max_length=250, choices=CHOICE_BARRIOS, null=True, blank=True)
    localidad       = models.CharField(max_length=250, choices=CHOICE_LOCALIDAD, null=True, blank=True)
    referente     = models.CharField(max_length=40, null=True, blank=True)
    telefono        = models.IntegerField(null=True, blank=True)
    email           = models.EmailField(null=True, blank=True)
    activo          = models.BooleanField(default=True)
    obs             = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")

    def __str__(self):
        return (self.nombre)

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Organismo'
        verbose_name_plural = "Organismos"

    def get_absolute_url(self):
        return reverse('organismos_ver', kwargs={'pk': self.pk})


class PlanesSociales(models.Model):    
    nombre          = models.CharField(max_length=250)
    jurisdiccion    = models.CharField(max_length=50, choices=CHOICE_JURISDICCION)
    activo          = models.BooleanField(default=True)
    obs             = models.CharField(max_length=500, null=True, blank=True,default="Sin Observaciones")

    def __str__(self):
        return (self.nombre)

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()
        
    class Meta:
        ordering = ['nombre']
        verbose_name = 'PlanSocial'
        verbose_name_plural = "PlanesSociales"

    def get_absolute_url(self):
        return reverse('planessociales_ver', kwargs={'pk': self.pk})


#region------- EXTENSION DEL MODELO USER---------------------------------------------------------------------

#Agrego extrafields telefono y programa
class Usuarios(models.Model):
    '''
    Extensión del modelo USER
    '''
    usuario     = models.OneToOneField(User, on_delete= models.CASCADE )
    telefono    = models.CharField(max_length=30, null=True, blank=True)
    fk_programa = models.ForeignKey(Programas, on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return self.usuario.first_name+' '+self.usuario.last_name
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = "Usuarios"
        

#endregion ------------------FIN EXTENSION USER MODEL-----------------------------------------------------


#region ------- DESTINATARIOS---------------------------------------------------------------------------------

class Destinatarios(models.Model):
    '''
    Destinatarios para posteriores uso en envio de mails, alertas, etc.
    '''    
    nombre      = models.CharField(max_length=100)
    email       = models.EmailField()
    referencia  = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return (self.nombre)
        
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Destinatario'
        verbose_name_plural = "Destinatarios"


#TODO En la vista o en el form, validar que no se pueda guardar el grupo vacío: o tiene al menos un destinatario o usuario
class GruposDestinatarios(models.Model):
    '''
    Grupos de Destinatarios, que puede contener tanto destinatarios externos (mail) como usuarios del sistema.
    La finalidad es su uso en envio de mails, alertas, etc.
    '''     
    nombre              = models.CharField(max_length=250)
    m2m_destinatarios   = models.ManyToManyField(Destinatarios,blank=True)
    m2m_usuarios        = models.ManyToManyField(Usuarios,blank=True)
    obs                 = models.CharField(max_length=500, null=True, blank=True,default="Sin Descripción")

    def __str__(self):
        return (self.nombre)    
            
    class Meta:
        ordering = ['nombre']
        verbose_name = 'GrupoDestinatarios'
        verbose_name_plural = "GruposDestinatarios"



#endregion ---------------------fin Tablas DESTINATARIOS------------------------------------------------------------------


#region-------- TIPO DE ALERTAS-------------------------------------------------------------------------------

class TipoAlertas(models.Model):
    '''
    Descripciones cortas para distintos tipos de alertas que cada servicio requiera.
    ''' 
    nombre          = models.CharField(max_length=250)
    obs             = models.CharField(max_length=500, null=True, blank=True,default='Sin Observaciones')

    def __str__(self):
        return (self.nombre)
    

    class Meta:
        ordering = ['nombre']
        verbose_name = 'TipoAlertas'
        verbose_name_plural = 'TiposAlertas'

    def get_absolute_url(self):
        return reverse('tipoalertas_ver', kwargs={'pk': self.pk})

#endregion--------FIN  ALERTAS---------------------------------------------------------------------------------


#region ------- CRITERIOS DE VULNERABILIDAD (para crear indices como el IVI/IVIJ/RAIJ y otros)----------------------

class SujetosCriterios(models.Model):
    '''
    Sujetos hacia quienes se aplicara, posteriormente, un criterio de vulnerabilidad. Por ejemplo: Embarazadas, Madres 
    o Cuidadores principales, bebés, adolescentes, etc.
    '''  
    nombre  = models.CharField(max_length=70)

    def __str__(self):
        return (self.nombre)
        
    class Meta:
        ordering = ['nombre']
        verbose_name = 'SujetoCriterios'
        verbose_name_plural = "SujetosCriterios"


class Criterios(models.Model):  
    '''
    Criterios de vulnerabilidad que seran posteriormente utilizados en la conformacion de INDICES (Ej. IVI).
    Cada criterio debe apuntar a un sujeto específico.
    '''   
    nombre                  = models.CharField(max_length=250)
    sujeto_de_aplicacion    = models.ForeignKey(SujetosCriterios,on_delete=models.SET_NULL,blank=True, null=True)
    activo                  = models.BooleanField(default=True)
    obs                     = models.CharField(max_length=500, null=True, blank=True,default="Sin Observaciones")

    def __str__(self):
        return (self.nombre)

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()
        
    class Meta:
        ordering = ['sujeto_de_aplicacion']
        verbose_name = 'Criterio'
        verbose_name_plural = "Criterios"

    def get_absolute_url(self):
        return reverse('criterios_ver', kwargs={'pk': self.pk})


class Indice(models.Model):
    '''
    **INDICES DE VULNERABILIDAD**

    Agrupan determinados criterios, les agrega puntaje y riesgo en la tabla puente 'IndiceCriterios',
    acorde a las necesidades que cada servicio/programa requiera.
    A su vez, un mismo índice puede ser utilizado por más de un programa.
    ''' 
    nombre              = models.CharField(max_length=250)
    m2m_criterios       = models.ManyToManyField(Criterios, through='IndiceCriterios')
    m2m_programas       = models.ManyToManyField(Programas)
    obs                 = models.CharField(max_length=500, null=True, blank=True,default="Sin Observaciones")
    activo              = models.BooleanField(default=True)

    def __str__(self):
        return (self.nombre)

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        verbose_name = 'Indice'
        verbose_name_plural = 'Indices'

    def get_absolute_url(self):
        return reverse('indice_ver', kwargs={'pk': self.pk})


#TODO se podria validar en forms que el numero sea dentro de un rango (ej 1 a 5)
class IndiceCriterios(models.Model):
    '''
    Tabla puente 'IndiceCriterios' que agrega campos eztras en la conformación de un índice,
    acorde a las necesidades que cada servicio/programa requiera.
    El campo 'impacto' alude a la valoracion que corresponda, en ese indice particular, ese criterio.
    el campo 'mejora' alude a si es posible, en ese indice particular, mejorar la puntuación con intervecniones programáticas 
    de los servicios.
    '''
    fk_criterio  = models.ForeignKey(Criterios, on_delete=models.PROTECT)
    fk_indice    = models.ForeignKey(Indice, on_delete=models.CASCADE)   
    puntaje      = models.PositiveSmallIntegerField(default=0)
    impacto      = models.CharField(max_length=10, choices=CHOICE_IMPACTO_CRITERIO)
    mejora       = models.BooleanField(default=False)
    activo       = models.BooleanField(default=True)

    

    def __str__(self):
        return f'{self.fk_criterio} - Impacto: {self.impacto}'

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        verbose_name = 'IndiceCriterios'
        verbose_name_plural = 'IndicesCriterios'

    def get_absolute_url(self):
        return reverse('indicecriterios_ver', kwargs={'pk': self.pk})

#endregion ---------------------FIN CRITERIOS DE VULNERABILIDAD---------------------------------------------------

