from django.urls import path, include
from .views import indexView, login_view, logout_view, registro_view, VehiculoCreateView , listar_vehiculo
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import permission_required
urlpatterns = [

    path('', indexView, name='index'), #VIEWS INDEX HASTA AQUI LA GUIA
    path('login/', login_view , name='login'),
    path('listar/', listar_vehiculo, name='listar_vehiculo'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', registro_view, name="registro"),
    path('vehiculo/add/', VehiculoCreateView.as_view(), name='vehiculo_add'),
    
]
handler403 = 'vehiculo.views.error_403'
