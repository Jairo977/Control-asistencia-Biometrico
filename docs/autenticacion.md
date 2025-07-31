# Documentación de Autenticación y Roles

## ¿Cómo funciona la autenticación?
- El sistema usa el modelo de usuario extendido de Django (`Usuario`), con roles (`admin`, `user`).
- El login y logout usan las vistas estándar de Django.
- El acceso a vistas sensibles (dashboard admin, configuración) está protegido con decoradores `@login_required` y validación de rol.
- Las contraseñas se almacenan con hash seguro.

## Cambiar credenciales
- Desde la vista de configuración, cualquier usuario puede cambiar su usuario y contraseña.
- El formulario valida que el usuario sea único y que la contraseña cumpla requisitos mínimos.

## ¿Cómo agregar un nuevo rol o permiso?
- Edita el modelo `Usuario` en `models.py` y agrega el nuevo rol en la tupla `ROLES`.
- Ajusta los decoradores y validaciones en las vistas para el nuevo rol.

---

**Ejemplo:**
Para que solo los usuarios con rol `supervisor` accedan a una vista:
```python
from django.contrib.auth.decorators import login_required
@login_required
def vista_supervisor(request):
    if not request.user.rol == 'supervisor':
        return redirect('no_autorizado')
    # lógica de la vista
```
