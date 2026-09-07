from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from urllib.parse import urlencode
from .models import Paciente
from .models import Expediente
from .forms import PacienteForm
from .forms import ExpedienteForm
from .services import buscar_cie
from datetime import date
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Vista personalizada de login para detectar si no hay usuarios y mostrar un mensaje.
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['no_users'] = not User.objects.exists()
        return kwargs

# Vista para crear el primer usuario cuando la aplicación no tiene cuentas registradas.
def register_initial_user(request):
    if User.objects.exists():
        return redirect('login')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Usuario creado correctamente. Ya puedes iniciar sesión.'
            )
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {
            'form': form
        }
    )


# Función de utilidad para saber si el usuario tiene permisos de fisioterapeuta.
# Se usa para habilitar o deshabilitar acciones de edición de expedientes.
def es_fisioterapeuta(user):

    return (
        user.is_superuser
        or
        user.groups.filter(
            name='Fisioterapeuta'
        ).exists()
    )


# Vista principal del dashboard con estadísticas generales y agenda del día.
@login_required
def inicio(request):

    total_pacientes = Paciente.objects.count()

    total_citas = Expediente.objects.count()

    citas_hoy = Expediente.objects.filter(
        fecha=date.today()
    ).count()

    agenda_hoy = Expediente.objects.filter(
        fecha=date.today()
    ).order_by('hora')

    return render(
        request,
        'index.html',
        {
            'total_pacientes': total_pacientes,
            'total_citas': total_citas,
            'citas_hoy': citas_hoy,
            'agenda_hoy': agenda_hoy
        }
    )


# Lista todas las citas registradas ordenadas por fecha y hora.
@login_required
def lista_citas(request):

    citas = Expediente.objects.all().order_by(
        '-fecha',
        '-hora'
    )

    return render(
        request,
        'appointments/lista.html',
        {
            'citas': citas
        }
    )


# Muestra únicamente las citas programadas para el día de hoy.
@login_required
def citas_hoy(request):

    citas = Expediente.objects.filter(
        fecha=date.today()
    ).order_by(
        'hora'
    )

    return render(
        request,
        'appointments/hoy.html',
        {
            'citas': citas
        }
    )


# Lista todos los pacientes registrados.
@login_required
def lista_pacientes(request):

    pacientes = Paciente.objects.all()

    return render(
        request,
        'patients/lista.html',
        {
            'pacientes': pacientes
        }
    )


# Crea un nuevo paciente usando el formulario y redirige a la lista de pacientes.
@login_required
def crear_paciente(request):

    if request.method == 'POST':

        form = PacienteForm(
            request.POST
        )

        form.save()

        messages.success(
            request,
            'Paciente registrado correctamente'
        )

        return redirect(
            'lista_pacientes'
        )

    else:

        form = PacienteForm()

    return render(
        request,
        'patients/crear.html',
        {
            'form': form
        }
    )


# Muestra el expediente de un paciente y evalúa si el usuario puede editarlo.
@login_required
def ver_expediente(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    expedientes = Expediente.objects.filter(
        paciente=paciente
    ).order_by('-fecha', '-hora')

    return render(
        request,
        'records/lista.html',
        {
            'paciente': paciente,
            'expedientes': expedientes,
            'puede_editar': es_fisioterapeuta(request.user)
        }
    )


# Crea un nuevo expediente para un paciente. Si el paciente tiene correo, envía confirmación por email.
@login_required
def crear_expediente(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        form = ExpedienteForm(
            request.POST
        )

        if form.is_valid():

            expediente = form.save(
                commit=False
            )

            expediente.paciente = paciente

            expediente.codigo_cie = form.cleaned_data.get(
                'codigo_cie'
            )

            expediente.diagnostico = form.cleaned_data.get(
                'diagnostico'
            )

            expediente.nota_adicional = form.cleaned_data.get(
                'nota_adicional'
            )

            expediente.save()

            # Si el paciente tiene correo electrónico, preparar y enviar la confirmación.
            if paciente.correo:
                subject = 'Confirmación de cita - Clínica de Fisioterapia Arial'
                context = {
                    'paciente': paciente,
                    'expediente': expediente,
                }
                html_message = render_to_string(
                    'emails/confirmacion_cita.html',
                    context
                )
                plain_message = strip_tags(html_message)
                email = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [paciente.correo]
                )
                email.attach_alternative(html_message, 'text/html')
                try:
                    email.send(fail_silently=False)
                    messages.success(
                        request,
                        'Cita registrada correctamente y se envió la confirmación al correo del paciente.'
                    )
                except Exception:
                    messages.warning(
                        request,
                        'Cita registrada correctamente, pero no se pudo enviar el correo de confirmación. Verifica la configuración de correo.'
                    )
            else:
                messages.success(
                    request,
                    'Cita registrada correctamente, pero el paciente no tiene correo registrado.'
                )

            return redirect(
                'ver_expediente',
                id=paciente.id
            )

    else:

        # Si no se envía el formulario, se precargan valores opcionales desde query string.
        initial = {}

        if request.GET.get('codigo'):
            initial['codigo_cie'] = request.GET.get('codigo')

        if request.GET.get('diagnostico'):
            initial['diagnostico'] = request.GET.get('diagnostico')

        if request.GET.get('fecha'):
            initial['fecha'] = request.GET.get('fecha')

        if request.GET.get('hora'):
            initial['hora'] = request.GET.get('hora')

        if request.GET.get('nota_adicional'):
            initial['nota_adicional'] = request.GET.get('nota_adicional')

        form = ExpedienteForm(initial=initial)

    return render(
        request,
        'records/crear.html',
        {

            'form': form,

            'paciente': paciente

        }
    )

# Vista de edición de un expediente. Solo la puede usar un fisioterapeuta o superusuario.
@login_required
@user_passes_test(es_fisioterapeuta)
def editar_expediente(request, id):

    expediente = get_object_or_404(
        Expediente,
        id=id
    )

    if request.method == 'POST':

        # Actualiza el expediente existente sin permitir cambiar fecha u hora.
        form = ExpedienteForm(
            request.POST,
            instance=expediente
        )

        form.fields['fecha'].disabled = True
        form.fields['hora'].disabled = True

        if form.is_valid():

           form.save()

        messages.success(
            request,
            'Expediente actualizado correctamente'
        )

        return redirect(
            'ver_expediente',
            id=expediente.paciente.id
        )

    else:

        initial = {}

        if request.GET.get('codigo'):
            initial['codigo_cie'] = request.GET.get('codigo')

        if request.GET.get('diagnostico'):
            initial['diagnostico'] = request.GET.get('diagnostico')

        if request.GET.get('nota_adicional'):
            initial['nota_adicional'] = request.GET.get('nota_adicional')

        form = ExpedienteForm(
            instance=expediente,
            initial=initial
        )

        form.fields['fecha'].disabled = True
        form.fields['hora'].disabled = True

    return render(
        request,
        'records/editar.html',
        {
            'form': form,
            'expediente': expediente,
            'puede_editar': es_fisioterapeuta(request.user)
        }
    )

# Busca diagnósticos CIE por término y muestra los resultados para un paciente.
@login_required
def buscar_diagnostico(request, paciente_id):

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    resultados = []

    query = request.GET.get('q')

    if query:

        resultados = buscar_cie(query)

    return render(
        request,
        'diagnostics/busqueda.html',
        {

            'resultados': resultados,

            'paciente': paciente,

            'next': request.GET.get('next', '')

        }
    )


# Guarda el diagnóstico seleccionado en el expediente y redirige al contexto anterior.
@login_required
def agregar_diagnostico(request, paciente_id):

    codigo = request.GET.get('codigo')
    diagnostico = request.GET.get('diagnostico')
    nota_adicional = request.GET.get('nota_adicional')
    next_url = request.GET.get('next')

    if not next_url:
        next_url = reverse('ver_expediente', args=[paciente_id])

    # Reenvía los parámetros de código, diagnóstico y nota adicional al URL de retorno.
    params = {}

    if codigo:
        params['codigo'] = codigo

    if diagnostico:
        params['diagnostico'] = diagnostico

    if nota_adicional:
        params['nota_adicional'] = nota_adicional

    if params:
        separator = '&' if '?' in next_url else '?'
        next_url = f"{next_url}{separator}{urlencode(params)}"

    return redirect(next_url)

# Devuelve las citas como eventos JSON para el calendario.
@login_required
def eventos(request):

    _ = request.method

    eventos = []

    citas = Expediente.objects.all()

    for cita in citas:

        eventos.append({

            'title': f'{cita.hora} - {cita.paciente.nombre}',

            'start': f'{cita.fecha}T{cita.hora}',

        })

    return JsonResponse(
        eventos,
        safe=False
    )