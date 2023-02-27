
from django.contrib.auth.mixins import PermissionRequiredMixin


# Clase para verificar al mismo tiempo usuario logeado y permisos
class PermissionsMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        self.permission_denied_message = 'No posee permisos para realizar la acción'
        return super(PermissionsMixin, self).handle_no_permission()