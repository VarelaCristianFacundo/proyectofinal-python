from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    PresupuestoFormulario,
    BusquedaPresupuestoForm,
    SignupForm,
    ColaboradorFormulario,
    ClienteFormulario,
    UserEditForm,
    AvatarFormulario,
)
from .models import Presupuesto, Colaborador, AsignacionPresupuesto, Avatar
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Subquery
from django.core.exceptions import ObjectDoesNotExist  # Importa ObjectDoesNotExist


# Create your views here.


def home(req):
    try:
        avatar = Avatar.objects.get(user=req.user.id)
        return render(req, "home.html", {"url_avatar": avatar.imagen.url})
    except:
        return render(
            req,
            "home.html",
            {
                "url_avatar": "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"
            },
        )


def loginView(req):
    if req.method == "POST":
        miFormulario = AuthenticationForm(req, data=req.POST)

        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario = data["username"]
            psw = data["password"]
            user = authenticate(username=usuario, password=psw)

            if user:
                login(req, user)
                url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"
                if req.user.is_authenticated:
                    try:
                        avatar = Avatar.objects.get(user=req.user)
                        url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
                    except ObjectDoesNotExist:
                        pass  # Maneja el caso en que no exista un avatar para el usuario
                    except Avatar.MultipleObjectsReturned:
                        avatars = Avatar.objects.filter(user=req.user)
                        avatar = avatars.first()
                        url_avatar = (
                            avatar.imagen.url
                        )  # Obtiene la URL del primer avatar
                return render(
                    req,
                    "Home.html",
                    {
                        "url_avatar": url_avatar,
                    },
                )

        return render(
            req,
            "Home.html",
            {"mensaje": f"Datos incorrectos"},
        )
    else:
        url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"
        miFormulario = AuthenticationForm()
        return render(
            req,
            "login.html",
            {
                "miFormulario": miFormulario,
                "url_avatar": url_avatar,
            },
        )


def signup_view(req):
    if req.method == "POST":
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect("Home")
    else:
        form = SignupForm()
    return render(req, "signup.html", {"form": form})


def register(req):
    if req.method == "POST":
        miFormulario = UserCreationForm(req.POST)

        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario = data["username"]
            miFormulario.save()
            return render(
                req, "Home.html", {"mensaje": f"Usuario {usuario} creado con éxito!"}
            )

        return render(req, "Home.html", {"mensaje": f"Formulario inválido"})
    else:
        miFormulario = UserCreationForm()
        return render(req, "registro.html", {"miFormulario": miFormulario})


@login_required
def listar_presupuestos(req):
    form = BusquedaPresupuestoForm()
    presupuestos = Presupuesto.objects.all()
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar

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
        {
            "presupuestos": presupuestos,
            "form": form,
            "url_avatar": url_avatar,
        },  # Pasa la URL del avatar a la plantilla
    )


def presupuestoFormulario(req):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"
    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar
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
        presupuestoFormulario = PresupuestoFormulario({"url_avatar": url_avatar})

    print(presupuestoFormulario)
    return render(
        req,
        "presupuestoFormulario.html",
        {"presupuestoFormulario": presupuestoFormulario, "url_avatar": url_avatar},
    )


# Vista para modificar un presupuesto
@login_required
def modificar_presupuesto(req, presupuesto_id):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar

    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id)

    if req.method == "POST":
        form = PresupuestoFormulario(req.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            return redirect("ListarPresupuestos")
    else:
        form = PresupuestoFormulario(instance=presupuesto)

    return render(
        req,
        "modificar_presupuesto.html",
        {
            "form": form,
            "url_avatar": url_avatar,
        },
    )


# Vista para confirmar y eliminar un presupuesto
@login_required
def eliminar_presupuesto(req, presupuesto_id):
    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id)

    if req.method == "POST":
        presupuesto.delete()
        return redirect("ListarPresupuestos")

    return render(
        req,
        "eliminar_presupuesto.html",
        {
            "presupuesto": presupuesto,
            "url_avatar": url_avatar,
        },
    )


@login_required
def listar_colaboradores(req):
    colaboradores = Colaborador.objects.all()
    presupuestos_asignados = AsignacionPresupuesto.objects.values("presupuesto_id")
    presupuestos_disponibles = Presupuesto.objects.exclude(
        id__in=Subquery(presupuestos_asignados)
    )
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar

    if req.method == "POST":
        colaborador_id = req.POST.get("colaborador")
        presupuesto_id = req.POST.get("presupuesto")

        if colaborador_id and presupuesto_id:
            colaborador = Colaborador.objects.get(pk=colaborador_id)
            presupuesto = Presupuesto.objects.get(pk=presupuesto_id)

            asignacion = AsignacionPresupuesto(
                colaborador=colaborador, presupuesto=presupuesto
            )
            asignacion.save()

            return redirect("ListarColaboradores")

    return render(
        req,
        "listar_colaboradores.html",
        {
            "colaboradores": colaboradores,
            "presupuestos": presupuestos_disponibles,
            "url_avatar": url_avatar,
        },
    )


@staff_member_required(login_url="/app/login/")
def agregar_colaborador(req):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar

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
        {
            "colaboradorForm": colaboradorForm,
            "url_avatar": url_avatar,
        },
    )


@login_required
def asignar_presupuesto(req, presupuesto_id, colaborador_id):
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


def proyectos_asignados(req):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar
    colaboradores = Colaborador.objects.all()
    proyectos_asignados = {}

    if req.method == "POST":
        colaborador_id = req.POST.get("colaborador")
        if colaborador_id:
            colaborador = Colaborador.objects.get(id=colaborador_id)
            proyectos_asignados = colaborador.asignacionpresupuesto_set.all()

    return render(
        req,
        "proyectos_asignados.html",
        {
            "colaboradores": colaboradores,
            "proyectos_asignados": proyectos_asignados,
            "url_avatar": url_avatar,
        },
    )


def agregar_cliente(req):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar
    if req.method == "POST":
        cliente_form = ClienteFormulario(req.POST)

        if cliente_form.is_valid():
            cliente_form.save()
            return redirect("PresupuestoFormulario")
    else:
        cliente_form = ClienteFormulario()

    return render(
        req,
        "agregar_cliente.html",
        {
            "cliente_form": cliente_form,
            "url_avatar": url_avatar,
        },
    )


@login_required
def editar_perfil(req):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar

    usuario = req.user

    if req.method == "POST":
        miFormulario = UserEditForm(req.POST, instance=req.user)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.email = data["email"]
            usuario.set_password(data["password1"])
            usuario.save()
            return render(
                req,
                "Home.html",
                {
                    "mensaje": "Datos actualizados con éxito!",
                    "url_avatar": url_avatar,
                },
            )
        # En caso de que el formulario no sea válido, se mostrará el formulario nuevamente
        else:
            return render(
                req,
                "editarPerfil.html",
                {
                    "miFormulario": miFormulario,
                    "url_avatar": url_avatar,
                },
            )
    else:
        miFormulario = UserEditForm(instance=usuario)
        return render(
            req,
            "editarPerfil.html",
            {
                "miFormulario": miFormulario,
                "url_avatar": url_avatar,
            },
        )


@login_required
def agregar_avatar(req):
    url_avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=req.user)
            url_avatar = avatar.imagen.url  # Obtiene la URL del avatar
        except ObjectDoesNotExist:
            pass  # Maneja el caso en que no exista un avatar para el usuario
        except Avatar.MultipleObjectsReturned:
            avatars = Avatar.objects.filter(user=req.user)
            avatar = avatars.first()
            url_avatar = avatar.imagen.url  # Obtiene la URL del primer avatar
    try:
        avatar = Avatar.objects.get(user=req.user)
    except Avatar.DoesNotExist:
        avatar = "https://www.researchgate.net/profile/Maria-Monreal/publication/315108532/figure/fig1/AS:472492935520261@1489662502634/Figura-2-Avatar-que-aparece-por-defecto-en-Facebook.png"

    if req.method == "POST":
        miFormulario = AvatarFormulario(req.POST, req.FILES)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data

            if avatar:
                # Si el usuario ya tiene un avatar, actualiza la imagen existente
                avatar.imagen = data["imagen"]
                avatar.save()
            else:
                # Si el usuario no tiene un avatar, crea uno nuevo
                avatar = Avatar(user=req.user, imagen=data["imagen"])
                avatar.save()

            return render(
                req,
                "Home.html",
                {
                    "mensaje": "Avatar actualizado con éxito!",
                    "url_avatar": url_avatar,
                },
            )
    else:
        miFormulario = AvatarFormulario()
        return render(
            req,
            "agregarAvatar.html",
            {
                "miFormulario": miFormulario,
                "url_avatar": url_avatar,
            },
        )
