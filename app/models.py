from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Cliente(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"


class Servicio(models.Model):
    idioma = models.CharField(max_length=40)
    cantidadDeHojas = models.IntegerField()

    def __str__(self):
        return f"{self.idioma} - {self.cantidadDeHojas}"


class Presupuesto(models.Model):
    servicio = models.CharField(max_length=40)
    fechaDeEntrega = models.DateField()
    entregado = models.BooleanField()
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.servicio} - {self.fechaDeEntrega} - {self.entregado}"


class Colaborador(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"


class AsignacionPresupuesto(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Asignación de Presupuesto: {self.colaborador} - {self.presupuesto}"


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", blank=True, null=True)
