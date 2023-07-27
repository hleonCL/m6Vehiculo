from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VehiculoForm, RegistroUsuarioForm 
from django.http import HttpResponse, HttpResponseRedirect
from tokenize import PseudoExtras
from django.contrib.auth import login, authenticate , logout 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from .models import vehiculo
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.views.generic.edit import CreateView
from django.views.generic import ListView

 
def error_403(request, exception):
    return render(request, '403.html', status=403)


# Create your views here.

def indexView(request):
    template_name = 'index.html'
    return render(request, template_name)

class VehiculoCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'app_name.add_vehiculomodel'
    model = vehiculo
    fields = ['marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio']
    template_name = 'addform.html'

    def get_success_url(self):
        return '/vehiculo/add/'

class AgregarVehiculo(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    raise_exception = True
    permission_required = 'vehiculo.visualizar_catalogo'
    template_name = 'addform.html'

    def addVehiculo(self, request):
        form = VehiculoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form = VehiculoForm()
            messages.success(request, '¡Los datos se han procesado Exitosamente!')

            return render(request, "addform.html", {'form': form })
        else:
            return render(request, "addform.html", {'form': form })

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Get the permission object
            permission = Permission.objects.get(codename='visualizar_catalogo')

            # Add the permission to the new user
            user.user_permissions.add(permission)

            messages.success(request, "Usuario registrado correctamente.")
            return HttpResponseRedirect('/listar/')
        messages.error(request, "Registro invalido. Algunos datos incorrectos. Verifique ")
    
    form= RegistroUsuarioForm()
    context = {"register_form": form }
    return render(request, 'registro.html', context)


def listar_vehiculo(request):
    vehiculos = vehiculo.objects.all()
    context = {'lista_vehiculos': vehiculos}
    return render (request, 'lista.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, "Se ha Cerrado la sesión satisfactoriamente.")
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Iniciaste sesion como: {username}.")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "Invalido username o password.")
        else:
            messages.error(request, "Invalido username o password.")
    form = AuthenticationForm()
    context = {"login_form": form} 
    return render(request, "login.html", context) 


from django.contrib.auth.models import Permission

def listar_permisos(request):
    permissions = Permission.objects.all()
    return render(request, 'lista_permisos.html', {'permissions': permissions})
