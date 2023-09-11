from django import forms
from .models import Cliente


class PresupuestoFormulario(forms.Form):
    servicio = forms.CharField(max_length=40)
    fechaDeEntrega = forms.DateField()
    cantidad = forms.IntegerField()
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
