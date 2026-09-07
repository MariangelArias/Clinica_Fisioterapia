from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


# Definición de rutas de URL para la aplicación.
urlpatterns = [
    path(
        '',
        views.inicio,
        name='home'
    ),

    path(
        'inicio/',
        views.inicio,
        name='inicio'
    ),

    path(
        'pacientes/',
        views.lista_pacientes,
        name='lista_pacientes'
    ),

    path(
        'pacientes/crear/',
        views.crear_paciente,
        name='crear_paciente'
    ),

    path(
        'pacientes/<int:id>/expediente/',
        views.ver_expediente,
        name='ver_expediente'
    ),

    path(
        'pacientes/<int:id>/expediente/crear/',
        views.crear_expediente,
        name='crear_expediente'
    ),

    # Rutas para crear y editar expedientes de pacientes.
    path(
        'expediente/<int:id>/editar/',
        views.editar_expediente,
        name='editar_expediente'
    ),

    path(
        'paciente/<int:paciente_id>/cie/',
        views.buscar_diagnostico,
        name='cie'
    ),

    path(
        'paciente/<int:paciente_id>/agregar-cie/',
        views.agregar_diagnostico,
        name='agregar_diagnostico'
    ),

    path(
        'eventos/',
        views.eventos,
        name='eventos'
    ),

    path(
    'citas/',
    views.lista_citas,
    name='lista_citas'
    ),

    path(
        'citas/hoy/',
        views.citas_hoy,
        name='citas_hoy'
    ),

    # Autenticación: login, registro inicial y logout.
    path(
        'login/',
        views.CustomLoginView.as_view(),
        name='login'
    ),

    path(
        'register/',
        views.register_initial_user,
        name='register'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'

    ),
     path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/password_reset/done/'
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/reset/done/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

]