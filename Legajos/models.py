from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User
from .choices import *
from Inicio.models import *


class Legajos(models.Model):
    apellido            = models.CharField(max_length=250)    
    nombre              = models.CharField(max_length=250)    
    fecha_nacimiento    = models.DateField()    
    tipo_doc            = models.CharField(max_length=50, choices=CHOICE_TIPO_DOC)      
    documento           = models.CharField(max_length=50, default='')      
    sexo                = models.CharField(max_length=50, choices=CHOICE_SEXO)      
    nacionalidad        = models.CharField(max_length=50, choices=CHOICE_NACIONALIDAD, null=True, blank=True)      
    otra_nacionalidad   = models.CharField(max_length=50, null=True, blank=True)
    genero              = models.CharField(max_length=50, choices=CHOICE_GENERO, null=True, blank=True)    
    otro_genero         = models.CharField(max_length=50, choices=CHOICE_GENERO_PRONOMBRE,null=True, blank=True) 
    pronombre_genero    = models.CharField(max_length=50, null=True, blank=True) 
    estado_civil        = models.CharField(max_length=50, choices=CHOICE_ESTADO_CIVIL, null=True, blank=True)         
    calle               = models.CharField(max_length=250, null=True, blank=True)
    altura              = models.IntegerField(null=True, blank=True)
    piso                = models.CharField(max_length=100, null=True, blank=True)
    circuito            = models.CharField(max_length=100, choices= CHOICE_CIRCUITOS, null=True, blank=True)
    barrio              = models.CharField(max_length=100, choices= CHOICE_BARRIOS, null=True, blank=True)
    localidad           = models.CharField(max_length=250, choices=CHOICE_LOCALIDAD, null=True, blank=True)
    telefono            = models.IntegerField(null=True, blank=True)
    email               = models.EmailField(null=True, blank=True)
    foto                = models.ImageField(upload_to='legajos', default='../static/img/perfil.png',null=True, blank=True) 
    m2m_alertas         = models.ManyToManyField(TipoAlertas, through='LegajoAlertas',blank=True)
    m2m_familiares      = models.ManyToManyField('self', through='LegajoGrupoFamiliar',symmetrical=True,)
    obs                 = models.CharField(max_length=300,default="Sin Observaciones",blank=True,null=True)
    activo              = models.BooleanField(default=True)
    creado_por          = models.ForeignKey(Usuarios, related_name='creado_por', on_delete=models.PROTECT,blank=True,null=True)
    modificado_por      = models.ForeignKey(Usuarios, related_name='modificado_por', on_delete=models.PROTECT,blank=True,null=True)
    creado              = models.DateField(auto_now_add=True)
    modificado          = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - DNI: {self.documento} - Fecha de Nacimiento: {self.fecha_nacimiento} "
    
    def clean(self):
        if self.fecha_nacimiento > date.today():
            raise ValidationError('La fecha de termino debe ser menor al día de hoy.')
    
    def edad(self):
        edad=date.today() - self.fecha_nacimiento   
        return  edad

    def delete(self):
        if not (self.foto.name.endswith('perfil.png')):
            self.foto.delete() # borra la imagen fisica
        return super().delete()

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        ordering = ['apellido']
        verbose_name = 'Legajo'
        verbose_name_plural = 'Legajos'

    def get_absolute_url(self):
        return reverse('legajos_ver', kwargs={'pk': self.pk})


class LegajoGrupoFamiliar(models.Model):
    fk_legajo_1              = models.ForeignKey(Legajos, related_name='fk_legajo1', on_delete=models.CASCADE)
    vinculo                  = models.CharField(max_length=50, choices=CHOICE_VINCULO_FAMILIAR)
    estado_relacion          = models.CharField(max_length=50, choices=CHOICE_ESTADO_RELACION,null=True, blank=True)
    fk_legajo_2              = models.ForeignKey(Legajos, related_name='fk_legajo2', on_delete=models.CASCADE)
    vinculo_inverso          = models.CharField(max_length=50, choices=CHOICE_VINCULO_FAMILIAR)
    estado_relacion_inverso  = models.CharField(max_length=50, choices=CHOICE_ESTADO_RELACION, null=True, blank=True)
    conviven                 = models.BooleanField(default=True)
    obs                      = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")
    modificado               = models.DateField(auto_now=True)

    def __str__(self):
        return f"Legajo: {self.fk_legajo_1}- Vínculo: {self.vinculo} - Familiar: {self.fk_legajo_2} - Vínculo: {self.vinculo_inverso}"

    class Meta:
        ordering = ['fk_legajo_2']
        unique_together= ['fk_legajo_1','fk_legajo_2']
        verbose_name = 'LegajoGrupoFamiliar'
        verbose_name_plural = 'LegajosGrupoFamiliar'

    def get_absolute_url(self):
        return reverse('LegajoGrupoFamiliar_ver', kwargs={'pk': self.pk})


#region--------------LEGAJO - ALERTAS-----------------------------------------------------------------------------------------

    
class LegajoAlertas(models.Model):
    fk_tipo_alerta  = models.ForeignKey(TipoAlertas, related_name='tipoalerta', on_delete=models.PROTECT)
    fk_legajo       = models.ForeignKey(Legajos, related_name='legajoalerta', on_delete=models.CASCADE)
    fecha_inicio    = models.DateField(auto_now=True)
    activo          = models.BooleanField(default=True)
    programa        = models.ForeignKey(Programas, related_name='alerta_desde_programa',on_delete=models.PROTECT, null=True, blank=True)
    motivo_inicio   = models.CharField(max_length=300, null=True, blank=True)
    motivo_fin      = models.CharField(max_length=300, null=True, blank=True)
    fecha_fin       = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.fk_legajo} - Alerta: {self.fk_tipo_alerta}"

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'LegajoAlertas'
        verbose_name_plural = 'LegajosAlertas'

    def get_absolute_url(self):
        return reverse('legajoalertas_ver', kwargs={'pk': self.pk})


class HistorialLegajoAlertas(models.Model):
    fk_tipo_alerta  = models.ForeignKey(TipoAlertas, related_name='tipo_alerta', on_delete=models.PROTECT)
    fk_legajo       = models.ForeignKey(Legajos, related_name='legajo_alerta', on_delete=models.CASCADE)
    activo          = models.BooleanField()
    programa        = models.ForeignKey(Programas, related_name='alertadesdeprograma',on_delete=models.PROTECT, null=True, blank=True)
    accion          = models.CharField(max_length=30, null=True, blank=True)
    motivo_fin      = models.CharField(max_length=300, null=True, blank=True)
    motivo_inicio   = models.CharField(max_length=300, null=True, blank=True)
    fecha           = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.fk_legajo

    class Meta:
        verbose_name = 'HistorialLegajoAlertas'
        verbose_name_plural = 'HistorialesLegajoAlertas'

    def get_absolute_url(self):
        return reverse('historiallegajoalertas_ver', kwargs={'pk': self.pk})


@receiver(post_save, sender = LegajoAlertas)
def legajoalertas_is_created(sender, instance, created, **kwargs):
    if created:
        HistorialLegajoAlertas.objects.create(
            accion          ='CREACION',
            fk_tipo_alerta  =instance.fk_tipo_alerta,
            fk_legajo       =instance.fk_legajo    ,
            estado          =instance.activo       ,
            programa        =instance.programa     ,
            motivo_fin      =instance.motivo_fin   ,
            motivo_inicio   =instance.motivo_inicio,
        )
    else:
        HistorialLegajoAlertas.objects.create(
            accion          ='MODIFICACION',
            fk_tipo_alerta  =instance.fk_tipo_alerta,
            fk_legajo       =instance.fk_legajo    ,
            estado          =instance.activo       ,
            programa        =instance.programa     ,
            motivo_fin      =instance.motivo_fin   ,
            motivo_inicio   =instance.motivo_inicio,
        )


#endregion---------FIN LEGAJO ALERTAS---------------------------------------------------------------------------------------------


#region------------- DIMENSIONES--------------------------------------------------------------------------------------------------

class DimensionSalud(models.Model):
    fk_legajo               = models.OneToOneField(Legajos, on_delete=models.CASCADE)
    obra_social             = models.CharField(max_length=250,null=True, blank=True)   
    m2m_lugares_atencion    = models.ManyToManyField (Organismos,blank=True)  
    tipo_discapacidad       = models.CharField(max_length=500, choices=CHOICE_TIPO_DISCAPACIDAD,null=True, blank=True) 
    otra_discapacidad       = models.CharField(max_length=100, null=True, blank=True)
    tipo_enfermedad         = models.CharField(max_length=500, choices=CHOICE_TIPO_ENFERMEDAD,null=True, blank=True) #multiple
    otra_enfermedad         = models.CharField(max_length=100, null=True, blank=True)
    obs                     = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")
    creado                  = models.DateField(auto_now_add=True)
    modificado              = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fk_legajo}"

    class Meta:
        ordering = ['fk_legajo']
        verbose_name = 'DimensionSalud'
        verbose_name_plural = 'DimensionesSalud'

    def get_absolute_url(self):
        return reverse('dimensionsalud_ver', kwargs={'pk': self.pk})


class DimensionEducativa(models.Model):
    fk_legajo           = models.OneToOneField(Legajos, on_delete=models.CASCADE)
    max_nivel           = models.CharField(max_length=50, choices=CHOICE_NIVEL_EDUCATIVO,null=True, blank=True)   
    titulo              = models.CharField(max_length=250, null=True, blank=True)   
    institucion         = models.CharField(max_length=250, null=True, blank=True) 
    cursos              = models.CharField(max_length=300, null=True, blank=True) 
    obs                 = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")
    creado              = models.DateField(auto_now_add=True)
    modificado          = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fk_legajo}"

    class Meta:
        ordering = ['fk_legajo']
        verbose_name = 'DimensionEducativa'
        verbose_name_plural = 'DimensionesEducativas'

    def get_absolute_url(self):
        return reverse('dimensioneducativa_ver', kwargs={'pk': self.pk})


class DimensionVivienda(models.Model):
    fk_legajo           = models.OneToOneField(Legajos, on_delete=models.CASCADE)
    posesion            = models.CharField(max_length=50, choices=CHOICE_TIPO_POSESION_VIVIENDA,null=True, blank=True)   
    compartida          = models.BooleanField(default=False,help_text="Más de una familia en el lugar") 
    construccion        = models.CharField(max_length=50, choices=CHOICE_TIPO_CONSTRUCCION_VIVIENDA, null=True, blank=True)   
    estado              = models.CharField(max_length=50, choices=CHOICE_TIPO_ESTADO_VIVIENDA, null=True, blank=True)   
    ambientes           = models.IntegerField(null=True, blank=True) 
    convivientes        = models.IntegerField(null=True, blank=True) 
    obs                 = models.CharField(max_length=300, null=True, blank=True,default="Sin Observaciones")
    creado              = models.DateField(auto_now_add=True)
    modificado          = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fk_legajo}"

    class Meta:
        ordering = ['fk_legajo']
        verbose_name = 'DimensionVivienda'
        verbose_name_plural = 'DimensionesVivienda'

    def get_absolute_url(self):
        return reverse('dimensionvivienda_ver', kwargs={'pk': self.pk})


class DimensionEconomica(models.Model):
    fk_legajo           = models.OneToOneField(Legajos, on_delete=models.CASCADE)
    ingresos            = models.IntegerField(null=True, blank=True) 
    m2m_planes          = models.ManyToManyField (PlanesSociales, blank=True)      
    creado              = models.DateField(auto_now_add=True)
    modificado          = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fk_legajo}"

    class Meta:
        ordering = ['fk_legajo']
        verbose_name = 'DimensionEconomica'
        verbose_name_plural = 'DimensionesEconomicas'

    def get_absolute_url(self):
        return reverse('dimensioneconomia_ver', kwargs={'pk': self.pk})


class DimensionLaboral(models.Model):
    fk_legajo           = models.OneToOneField(Legajos, on_delete=models.CASCADE)
    situacion           = models.CharField(max_length=50, choices=CHOICE_SITUACION_LABORAL,null=True, blank=True)
    organizacion        = models.CharField(max_length=300, null=True, blank=True)      
    function            = models.CharField(max_length=300, null=True, blank=True)      
    creado              = models.DateField(auto_now_add=True)
    modificado          = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fk_legajo}"

    class Meta:
        ordering = ['fk_legajo']
        verbose_name = 'DimensionLaboral'
        verbose_name_plural = 'DimensionesLaborales'

    def get_absolute_url(self):
        return reverse('dimensionlaboral_ver', kwargs={'pk': self.pk})

#endregion-------------FIN DIMENSIONES-------------------------------------------------------------------------------------------------


#region--------------LEGAJOS/INDICES DE VULNERABILIDAD-----------------------------------------------------------------------------


class LegajoIndice(models.Model):
    fk_indice      = models.ForeignKey(Indice,on_delete=models.CASCADE)
    fk_legajo      = models.ForeignKey(Legajos, on_delete=models.CASCADE)
    mejora_puntaje = models.PositiveSmallIntegerField(null=True, blank=True)
    puntaje_total  = models.PositiveSmallIntegerField(null=True, blank=True)
    riesgo         = models.CharField(max_length=10, choices=CHOICE_NIVEL, null=True)
    obs            = models.CharField(max_length=300,default="Sin Observaciones", null=True, blank=True)
    fecha          = models.DateField(auto_now_add=True)



    def __str__(self):
        return f'{self.fk_legajo}'

    class Meta:
        verbose_name = 'LegajoIndice'
        verbose_name_plural = 'LegajosIndices'

    def get_absolute_url(self):
        return reverse('legajosindices_ver', kwargs={'pk': self.pk})


class HistorialLegajoIndice(LegajoIndice):
    accion       = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.fk_legajo

    class Meta:
        verbose_name = 'HistorialLegajoIndice'
        verbose_name_plural = 'HistorialesLegajoIndices'

    def get_absolute_url(self):
        return reverse('historiallegajoindice_ver', kwargs={'pk': self.pk})


@receiver(post_save, sender = LegajoIndice)
def legajoindice_is_created(sender, instance, created, **kwargs):
    if created:
        HistorialLegajoIndice.objects.create(
            accion          = 'CREACION',
        )
    else:
        HistorialLegajoIndice.objects.create(
            accion          = 'ACTUALIZACION',
        )

#endregion-----------FIN LEGAJOS/ INDICES DE VULNERABILIDAD-------------------------------------------------------------------------
