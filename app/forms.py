from django import forms
from .models import Cliente, Colaborador
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Presupuesto, Avatar
from django.utils import timezone
from django.core.exceptions import ValidationError


class PresupuestoFormulario(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ["servicio", "fechaDeEntrega", "cantidad", "cliente"]
        widgets = {
            "fechaDeEntrega": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_fechaDeEntrega(self):
        fecha_entrega = self.cleaned_data["fechaDeEntrega"]
        if fecha_entrega < timezone.now().date():
            raise ValidationError(
                "La fecha de entrega no puede ser anterior al día actual."
            )
        return fecha_entrega


class ColaboradorFormulario(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ["nombre", "apellido", "email"]


class ClienteFormulario(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "email"]


class BusquedaPresupuestoForm(forms.Form):
    consulta = forms.CharField(label="Buscar presupuesto por servicio", max_length=100)


class BusquedaColaboradorForm(forms.Form):
    consulta = forms.CharField(label="Buscar colaborador", max_length=100)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class UserEditForm(UserChangeForm):
    # Hago desaparecer la password y texto de ayuda
    password = forms.CharField(help_text="", widget=forms.HiddenInput(), required=False)

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2


class AvatarFormulario(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ("imagen",)
