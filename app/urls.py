from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="Home"),
    path("login/", loginView, name="Login"),
    path("signup/", signup_view, name="Signup"),  # Nueva URL para el registro
    path("presupuestoFormulario/", presupuestoFormulario, name="PresupuestoFormulario"),
    path("presupuestos/", listar_presupuestos, name="ListarPresupuestos"),
    path("agregar_colaborador/", agregar_colaborador, name="AgregarColaborador"),
    path("agregar_cliente/", agregar_cliente, name="AgregarCliente"),
    path(
        "modificar_presupuesto/<int:presupuesto_id>/",
        modificar_presupuesto,
        name="ModificarPresupuesto",
    ),
    path(
        "eliminar_presupuesto/<int:presupuesto_id>/",
        eliminar_presupuesto,
        name="EliminarPresupuesto",
    ),
    path("colaboradores/", listar_colaboradores, name="ListarColaboradores"),
    path(
        "asignar_presupuesto/<int:presupuesto_id>/<int:colaborador_id>/",
        asignar_presupuesto,
        name="AsignarPresupuesto",
    ),
    path("proyectos_asignados/", proyectos_asignados, name="proyectos_asignados"),
]
