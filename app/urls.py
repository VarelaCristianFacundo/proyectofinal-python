from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="Home"),
    path("login/", login, name="Login"),
    path("presupuestoFormulario/", presupuestoFormulario, name="PresupuestoFormulario"),
]
