from django import forms
from .models import Cliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PresupuestoFormulario(forms.Form):
    servicio = forms.CharField(max_length=40)
    fechaDeEntrega = forms.DateField()
    cantidad = forms.IntegerField()
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())


class BusquedaPresupuestoForm(forms.Form):
    consulta = forms.CharField(label="Buscar presupuesto", max_length=100)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
