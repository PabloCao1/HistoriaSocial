from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

#region------------LOGENTRY--------------------------------------------------------------------------
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"

#endregion----------------------------------------------------------------------------------------------------------


#region-----------USUARIOS---------------------------------------------------------------------------------------

class UsuariosInline(admin.StackedInline):
    model = Usuarios
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuariosInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#endregion-----------USUARIOS---------------------------------------------------------------------------------------



@admin.register(Secretarias)
class SecretariasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'obs')


@admin.register(Subsecretarias)
class SubsecretariasAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_secretaria', 'nombre', 'activo', 'obs')
    list_filter = ('fk_secretaria', 'activo')


@admin.register(Programas)
class ProgramasAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_subecretaria', 'nombre', 'activo', 'obs')
    list_filter = ('fk_subecretaria', 'activo')


@admin.register(Organismos)
class OrganismosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'tipo',
        'calle',
        'altura',
        'piso',
        'barrio',
        'localidad',
        'referente',
        'telefono',
        'email',
        'activo',
        'obs',
    )
    list_filter = ('activo',)


@admin.register(PlanesSociales)
class PlanesSocialesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'jurisdiccion', 'activo', 'obs')
    list_filter = ('activo',)

@admin.register(Destinatarios)
class DestinatariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'referencia')


class UsuariosInline(admin.TabularInline):
    model = GruposDestinatarios.m2m_usuarios.through
    extra = 1
class DestinatariosInline(admin.TabularInline):
    model = GruposDestinatarios.m2m_destinatarios.through
    extra = 1
@admin.register(GruposDestinatarios)
class GruposDestinatariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'obs')
    exclude = ('m2m_destinatarios','m2m_usuarios' )
    inlines = (DestinatariosInline, UsuariosInline,)


@admin.register(TipoAlertas)
class TipoAlertasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'obs')


@admin.register(SujetosCriterios)
class SujetosCriteriosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Criterios)
class CriteriosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'sujeto_de_aplicacion', 'activo', 'obs')
    list_filter = ('sujeto_de_aplicacion', 'activo')


class ProgramasInline(admin.TabularInline):
    model = Indice.m2m_programas.through
    extra = 1
class IndiceCriteriosInline(admin.TabularInline):
    model = IndiceCriterios
    extra = 1
@admin.register(Indice)
class IndiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'obs', 'activo')
    list_filter = ( 'nombre', 'activo',)
    inlines = (ProgramasInline, IndiceCriteriosInline)
    exclude = ('m2m_criterios', 'm2m_programas')

    
@admin.register(IndiceCriterios)
class IndiceCriteriosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fk_criterio',
        'fk_indice',
        'puntaje',
        'impacto',
        'mejora',
        'activo',
    )
    list_filter = ('fk_criterio', 'fk_indice', 'mejora', 'activo')