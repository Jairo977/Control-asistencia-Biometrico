# Control-asistencia-Biometrico

> Sistema profesional de control de asistencia biométrica con Django y SQL Server. Incluye autenticación, dashboards, reportes exportables y administración avanzada. Ideal para portafolio y despliegue empresarial.

---

## 🚀 ¿Qué hace este sistema?

- Autenticación de usuarios y gestión de roles (admin, user, superuser)
- Consulta y visualización de asistencia biométrica en tiempo real
- Exportación de reportes a PDF y Excel
- Panel de administración seguro para usuarios
- Sidebar y navegación responsiva según permisos
- Conexión directa a SQL Server (sin migraciones)
- Consultas optimizadas para alto volumen de datos

## 🏗️ Arquitectura y módulos principales

- `reportes/views.py`: Lógica de vistas, dashboards, reportes y exportaciones
- `reportes/db_utils.py`: Consultas SQL directas a la base biométrica
- `reportes/models.py`: Modelo de usuario extendido con roles
- `reportes/templates/`: HTMLs para cada sección (dashboard, reportes, admin, etc.)
- `docs/`: Documentación técnica detallada (vistas, modelos, autenticación, ejemplos)

Consulta la documentación técnica en la carpeta [`docs/`](docs/).

## ⚙️ Instalación y configuración rápida

1. Clona el repositorio:
	```bash
	git clone https://github.com/Jairo977/Control-asistencia-Biometrico.git
	cd Control-asistencia-Biometrico
	```
2. Instala dependencias:
	```bash
	pip install -r requirements.txt
	```
3. Configura la conexión a SQL Server en `reportes/db_utils.py`:
	```python
	DB_SERVER = 'TU_SERVIDOR_SQL'  # Ejemplo: '192.168.0.9\\ATIEMPO'
	DB_NAME = 'UTIME'
	DB_USER = 'tics2025'
	DB_PASSWORD = 'tics2025'
	```
	Asegúrate de tener instalado el driver ODBC 17 para SQL Server.
4. Ejecuta el servidor:
	```bash
	python manage.py runserver
	```

## 🧑‍💻 Personalización y extensión

- **Agregar campos a reportes:** Edita la consulta SQL en `db_utils.py` y el template correspondiente.
- **Cambiar el menú lateral:** Modifica `templates/sidebar.html` y ajusta los permisos con `{% if rol == 'admin' %}`.
- **Agregar un nuevo rol:** Edita el modelo `Usuario` en `models.py` y ajusta las vistas.
- **Cambiar el formato de exportación:** Edita las funciones de exportación en `views.py`.
- **Ver ejemplos y casos:** Consulta [`docs/ejemplos.md`](docs/ejemplos.md).

## 🔒 Seguridad y autenticación

- Login y logout protegidos por sesión y CSRF
- Roles y permisos en el modelo de usuario
- Panel de administración solo para superusuarios
- Contraseñas seguras (hash)
- Cambia tus credenciales desde la sección de configuración

## 📂 Estructura del proyecto

```
Control-asistencia-Biometrico/
├── manage.py
├── requirements.txt
├── README.md
├── docs/                  # Documentación técnica detallada
├── reportes/              # App principal
│   ├── db_utils.py        # Consultas SQL directas
│   ├── views.py           # Lógica de vistas y reportes
│   ├── models.py          # Modelo de usuario
│   ├── templates/         # HTMLs y frontend
│   └── ...
├── proyecto_biometrico/   # Configuración Django
└── ...
```

## 📖 Documentación técnica

- [`docs/arquitectura.md`](docs/arquitectura.md): Arquitectura y flujo general
- [`docs/vistas.md`](docs/vistas.md): Todas las vistas y rutas
- [`docs/modelos.md`](docs/modelos.md): Modelos y tablas externas
- [`docs/db_utils.md`](docs/db_utils.md): Funciones de acceso a la base
- [`docs/autenticacion.md`](docs/autenticacion.md): Autenticación y roles
- [`docs/exportacion.md`](docs/exportacion.md): Exportación de reportes
- [`docs/sidebar.md`](docs/sidebar.md): Personalización del menú
- [`docs/ejemplos.md`](docs/ejemplos.md): Casos prácticos y personalización

## 👨‍💻 Créditos y contacto

- Autor: Jairo977
- Email: tu.email@ejemplo.com
- Portafolio: https://github.com/Jairo977

---

¿Quieres adaptar este sistema a otra empresa, agregar módulos o integrarlo con otro biométrico? Lee la documentación y personaliza cualquier parte fácilmente.