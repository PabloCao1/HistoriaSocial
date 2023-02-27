# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


@admin.register(Legajos)
class LegajosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'apellido',
        'nombre',
        'fecha_nacimiento',
        'nacionalidad',
        'otra_nacionalidad',
        'tipo_doc',
        'documento',
        'sexo',
        'genero',
        'otro_genero',
        'pronombre_genero',
        'estado_civil',
        'calle',
        'altura',
        'piso',
        'circuito',
        'barrio',
        'localidad',
        'telefono',
        'email',
        'foto',
        'obs',
        'activo',
        'creado_por',
        'modificado_por',
        'creado',
        'modificado',
    )
    list_filter = (
        'fecha_nacimiento',
        'activo',
        'creado_por',
        'modificado_por',
        'creado',
        'modificado',
    )
    raw_id_fields = ('m2m_alertas', 'm2m_familiares')


@admin.register(LegajoGrupoFamiliar)
class LegajoGrupoFamiliarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_legajo_1',
        'vinculo',
        'estado_relacion',
        'fk_legajo_2',
        'vinculo_inverso',
        'estado_relacion_inverso',
        'conviven',
        'obs',
        'modificado',
    )
    list_filter = ('fk_legajo_1', 'fk_legajo_2', 'conviven', 'modificado')


@admin.register(LegajoAlertas)
class LegajoAlertasAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_tipo_alerta',
        'fk_legajo',
        'fecha_inicio',
        'activo',
        'programa',
        'motivo_inicio',
        'motivo_fin',
        'fecha_fin',
    )
    list_filter = (
        'fk_tipo_alerta',
        'fk_legajo',
        'fecha_inicio',
        'activo',
        'programa',
        'fecha_fin',
    )


@admin.register(HistorialLegajoAlertas)
class HistorialLegajoAlertasAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_tipo_alerta',
        'fk_legajo',
        'activo',
        'programa',
        'accion',
        'motivo_fin',
        'motivo_inicio',
        'fecha',
    )
    list_filter = (
        'fk_tipo_alerta',
        'fk_legajo',
        'activo',
        'programa',
        'fecha',
    )


@admin.register(DimensionSalud)
class DimensionSaludAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_legajo',
        'obra_social',
        'tipo_discapacidad',
        'otra_discapacidad',
        'tipo_enfermedad',
        'otra_enfermedad',
        'obs',
        'creado',
        'modificado',
    )
    list_filter = ('fk_legajo', 'creado', 'modificado')
    raw_id_fields = ('m2m_lugares_atencion',)


@admin.register(DimensionEducativa)
class DimensionEducativaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_legajo',
        'max_nivel',
        'titulo',
        'institucion',
        'cursos',
        'obs',
        'creado',
        'modificado',
    )
    list_filter = ('fk_legajo', 'creado', 'modificado')


@admin.register(DimensionVivienda)
class DimensionViviendaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_legajo',
        'posesion',
        'compartida',
        'construccion',
        'estado',
        'ambientes',
        'convivientes',
        'obs',
        'creado',
        'modificado',
    )
    list_filter = ('fk_legajo', 'compartida', 'creado', 'modificado')


@admin.register(DimensionEconomica)
class DimensionEconomicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_legajo', 'ingresos', 'creado', 'modificado')
    list_filter = ('fk_legajo', 'creado', 'modificado')
    raw_id_fields = ('m2m_planes',)


@admin.register(DimensionLaboral)
class DimensionLaboralAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_legajo',
        'situacion',
        'organizacion',
        'function',
        'creado',
        'modificado',
    )
    list_filter = ('fk_legajo', 'creado', 'modificado')


@admin.register(LegajoIndice)
class LegajoIndiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_indice',
        'fk_legajo',
        'mejora_puntaje',
        'puntaje_total',
        'riesgo',
        'obs',
        'fecha',
    )
    list_filter = ('fk_indice', 'fk_legajo', 'fecha')


@admin.register(HistorialLegajoIndice)
class HistorialLegajoIndiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_indice',
        'fk_legajo',
        'mejora_puntaje',
        'puntaje_total',
        'riesgo',
        'obs',
        'fecha',
        'accion',
    )
    list_filter = ('fk_indice', 'fk_legajo', 'fecha')