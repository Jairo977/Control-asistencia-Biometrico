# Documentación del Sidebar y Navegación

## ¿Cómo funciona el sidebar?
- El sidebar está en `reportes/templates/sidebar.html`.
- Muestra enlaces según el rol del usuario (admin, user, superuser).
- Los íconos y tooltips usan Bootstrap Icons.
- El menú es responsivo y se puede ocultar en móvil.

## ¿Cómo agregar o quitar un enlace?
- Edita el archivo `sidebar.html`.
- Agrega un nuevo `<a href="...">` con la URL y el ícono deseado.
- Para mostrar solo a admins, usa:
  ```django
  {% if rol == 'admin' or request.user.is_superuser %}
      ...enlace...
  {% endif %}
  ```

## ¿Cómo cambiar el orden o el nombre de un enlace?
- Simplemente mueve o edita el texto dentro del archivo `sidebar.html`.
