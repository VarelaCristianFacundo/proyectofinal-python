from django.db import models

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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.servicio} - {self.fechaDeEntrega} - {self.entregado}"


class Colaborador(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"
