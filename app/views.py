from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    PresupuestoFormulario,
    BusquedaPresupuestoForm,
    SignupForm,
    BusquedaColaboradorForm,
)
from .models import Presupuesto, Cliente, Colaborador, AsignacionPresupuesto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

# Create your views here.


def home(req):
    return render(req, "home.html")


def login(req):
    return render(req, "login.html")


def presupuesto(req):
    return render(req, "presupuestoFormulario.html")


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(
                "Home"
            )  # Puedes redirigir al usuario a la página que desees después del registro
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def listar_presupuestos(req):
    form = BusquedaPresupuestoForm()
    presupuestos = Presupuesto.objects.all()

    if req.method == "POST":
        form = BusquedaPresupuestoForm(req.POST)
        if form.is_valid():
            consulta = form.cleaned_data["consulta"]
            presupuestos = Presupuesto.objects.filter(
                servicio__icontains=consulta
            )  # Filtrar por servicio (ajusta según tus necesidades)

    return render(
        req, "listar_presupuestos.html", {"presupuestos": presupuestos, "form": form}
    )


def presupuestoFormulario(req):
    if req.method == "POST":
        presupuestoFormulario = PresupuestoFormulario(req.POST)

        if presupuestoFormulario.is_valid():
            data = presupuestoFormulario.cleaned_data

            # Obtén el cliente seleccionado del formulario
            cliente = data["cliente"]

            presupuesto = Presupuesto(
                servicio=data["servicio"],
                fechaDeEntrega=data["fechaDeEntrega"],
                cantidad=data["cantidad"],
                entregado=False,
                cliente=cliente,
            )
            presupuesto.save()

            return render(req, "home.html")
    else:
        presupuestoFormulario = PresupuestoFormulario()

    print(presupuestoFormulario)
    return render(
        req,
        "presupuestoFormulario.html",
        {"presupuestoFormulario": presupuestoFormulario},
    )


# Vista para modificar un presupuesto
def modificar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id)

    if request.method == "POST":
        form = PresupuestoFormulario(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            return redirect("ListarPresupuestos")
    else:
        form = PresupuestoFormulario(instance=presupuesto)

    return render(request, "modificar_presupuesto.html", {"form": form})


# Vista para confirmar y eliminar un presupuesto
def eliminar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id)

    if request.method == "POST":
        presupuesto.delete()
        return redirect("ListarPresupuestos")

    return render(request, "eliminar_presupuesto.html", {"presupuesto": presupuesto})


def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    presupuestos = Presupuesto.objects.all()

    if request.method == "POST":
        colaborador_id = request.POST.get("colaborador")
        presupuesto_id = request.POST.get("presupuesto")

        if colaborador_id and presupuesto_id:
            colaborador = Colaborador.objects.get(pk=colaborador_id)
            presupuesto = Presupuesto.objects.get(pk=presupuesto_id)

            # Crea una instancia de AsignacionPresupuesto y guárdala en la base de datos
            asignacion = AsignacionPresupuesto(
                colaborador=colaborador, presupuesto=presupuesto
            )
            asignacion.save()

            # Redirige o renderiza una respuesta después de realizar la asignación
            return redirect("ListarColaboradores")

    return render(
        request,
        "listar_colaboradores.html",
        {"colaboradores": colaboradores, "presupuestos": presupuestos},
    )


def asignar_presupuesto(request, presupuesto_id, colaborador_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id)
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)

    # Verifica si la asignación ya existe
    asignacion_existente = Asignacion.objects.filter(
        presupuesto=presupuesto, colaborador=colaborador
    ).exists()

    if not asignacion_existente:
        asignacion = Asignacion(presupuesto=presupuesto, colaborador=colaborador)
        asignacion.save()

    # Redirecciona
    return redirect("ListarPresupuestos")


def proyectos_asignados(request):
    colaboradores = Colaborador.objects.all()
    proyectos_asignados = {}

    if request.method == "POST":
        colaborador_id = request.POST.get("colaborador")
        if colaborador_id:
            colaborador = Colaborador.objects.get(id=colaborador_id)
            proyectos_asignados = colaborador.asignacionpresupuesto_set.all()

    return render(
        request,
        "proyectos_asignados.html",
        {"colaboradores": colaboradores, "proyectos_asignados": proyectos_asignados},
    )
