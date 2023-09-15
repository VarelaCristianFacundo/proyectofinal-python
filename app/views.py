from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    PresupuestoFormulario,
    BusquedaPresupuestoForm,
    SignupForm,
    ColaboradorFormulario,
    ClienteFormulario,
)
from .models import Presupuesto, Colaborador, AsignacionPresupuesto
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.db.models import Subquery


# Create your views here.


def home(req):
    return render(req, "home.html")


def login(req):
    if req.method == "POST":
        miFormulario = AuthenticationForm(req, data=req.POST)

        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario = data["username"]
            usuario.save()

            return render(req, "Home.html")

    else:
        miFormulario = ColaboradorFormulario()

    return render(req, "login.html")


def presupuesto(req):
    return render(req, "presupuestoFormulario.html")


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("Home")
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
            presupuestos = Presupuesto.objects.filter(servicio__icontains=consulta)

    if "borrar_filtros" in req.GET:
        presupuestos = (
            Presupuesto.objects.all()
        )  # Obtener todos los presupuestos sin filtro

    return render(
        req,
        "listar_presupuestos.html",
        {"presupuestos": presupuestos, "form": form},
    )


def presupuestoFormulario(req):
    if req.method == "POST":
        presupuestoFormulario = PresupuestoFormulario(req.POST)

        if presupuestoFormulario.is_valid():
            data = presupuestoFormulario.cleaned_data
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
    presupuestos_asignados = AsignacionPresupuesto.objects.values("presupuesto_id")
    presupuestos_disponibles = Presupuesto.objects.exclude(
        id__in=Subquery(presupuestos_asignados)
    )

    if request.method == "POST":
        colaborador_id = request.POST.get("colaborador")
        presupuesto_id = request.POST.get("presupuesto")

        if colaborador_id and presupuesto_id:
            colaborador = Colaborador.objects.get(pk=colaborador_id)
            presupuesto = Presupuesto.objects.get(pk=presupuesto_id)

            asignacion = AsignacionPresupuesto(
                colaborador=colaborador, presupuesto=presupuesto
            )
            asignacion.save()

            return redirect("ListarColaboradores")

    return render(
        request,
        "listar_colaboradores.html",
        {"colaboradores": colaboradores, "presupuestos": presupuestos_disponibles},
    )


def agregar_colaborador(req):
    if req.method == "POST":
        colaboradorForm = ColaboradorFormulario(req.POST)

        if colaboradorForm.is_valid():
            data = colaboradorForm.cleaned_data

            colaborador = Colaborador(
                nombre=data["nombre"],
                apellido=data["apellido"],
                email=data["email"],
            )
            colaborador.save()

            return redirect("ListarColaboradores")
    else:
        colaboradorForm = ColaboradorFormulario()

    return render(
        req,
        "agregar_colaborador.html",
        {"colaboradorForm": colaboradorForm},
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


def agregar_cliente(request):
    if request.method == "POST":
        cliente_form = ClienteFormulario(request.POST)

        if cliente_form.is_valid():
            cliente_form.save()
            return redirect("PresupuestoFormulario")
    else:
        cliente_form = ClienteFormulario()

    return render(
        request,
        "agregar_cliente.html",
        {"cliente_form": cliente_form},
    )
