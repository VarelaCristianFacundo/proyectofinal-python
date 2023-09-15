from django import forms
from .models import Cliente, Colaborador
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Presupuesto


class PresupuestoFormulario(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ["servicio", "fechaDeEntrega", "cantidad", "entregado", "cliente"]


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
