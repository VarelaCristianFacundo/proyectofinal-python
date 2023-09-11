from django.shortcuts import render
from .forms import PresupuestoFormulario, BusquedaPresupuestoForm
from .models import Presupuesto, Cliente

# Create your views here.


def home(req):
    return render(req, "home.html")


def login(req):
    return render(req, "login.html")


def presupuesto(req):
    return render(req, "presupuestoFormulario.html")


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

            return render(req, "presupuestoFormulario.html")
    else:
        presupuestoFormulario = PresupuestoFormulario()

    print(presupuestoFormulario)
    return render(
        req,
        "presupuestoFormulario.html",
        {"presupuestoFormulario": presupuestoFormulario},
    )
