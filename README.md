# Clínica de Fisioterapia

Sistema Django para la gestión clínica de fisioterapia: pacientes, expedientes, citas, diagnósticos CIE y autenticación.

## Descripción

Aplicación web en Django 6.0.4 con:
- Autenticación de usuarios (login / logout / registro inicial)
- Gestión de pacientes
- Creación y edición de expedientes clínicos
- Búsqueda y selección de diagnósticos CIE
- Calendario interactivo para agendar citas
- Modo oscuro persistente en el navegador
- Envío de correo de confirmación de cita

## Requisitos

- Python 3.14
- Django 6.0.4
- python-dotenv
- PyMySQL

## Instalación

1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Copiar `.env.example` a `.env` y completar los valores reales en tu equipo local.

No subas ese archivo a GitHub. Debe contener valores reales solo en tu equipo local.

## Variables de entorno

El proyecto carga variables desde `.env` usando `python-dotenv`.

Ejemplo mínimo de `.env`:

```env
SECRET_KEY=pon_aqui_una_clave_larga_y_aleatoria
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuración opcional de MySQL

Si deseas usar MySQL en lugar de SQLite, agrega estas variables:

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=tu_contraseña_real
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

En `fisioterapia_web/__init__.py` el proyecto intenta importar `MySQLdb` y usa `PyMySQL` como respaldo en caso de que no esté disponible.

## Base de datos por defecto

- Si `DB_ENGINE` está definida, el proyecto usa la base de datos configurada en `.env`.
- Si no, usa SQLite con `db.sqlite3` en la raíz del proyecto.

Para publicar en GitHub, elimina `db.sqlite3` del repositorio y crea una base vacía o solo migraciones.

## Migraciones

Ejecutar migraciones:

```powershell
python manage.py migrate
```

## Crear superusuario

```powershell
python manage.py createsuperuser
```

## Ejecutar el servidor

```powershell
python manage.py runserver
```

Luego abrir `http://127.0.0.1:8000/` en el navegador.

## Rutas útiles

- `/login/` — login
- `/inicio/` — página principal
- `/pacientes/` — lista de pacientes
- `/pacientes/crear/` — crear nuevo paciente
- `/citas/` — lista de citas
- `/citas/hoy/` — citas de hoy

## Notas importantes

- `LOGIN_URL` está configurado a `/login/`.
- `LOGIN_REDIRECT_URL` llega a `/inicio/`.
- El modo oscuro se guarda en `localStorage` del navegador mediante JavaScript.

## Estructura básica

- `fisioterapia_web/` — configuración Django
- `miapp/` — aplicación principal con vistas, modelos, servicios y plantillas
- `miapp/templates/` — plantillas HTML
- `miapp/static/css/estilos.css` — estilos y dark mode

## Email

La configuración SMTP está en `fisioterapia_web/settings.py` y usa Gmail:

- `EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`
- `EMAIL_HOST = 'smtp.gmail.com'`
- `EMAIL_PORT = 587`
- `EMAIL_USE_TLS = True`

También define `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` desde el `.env`.

## Validación rápida

```powershell
python manage.py check
```
