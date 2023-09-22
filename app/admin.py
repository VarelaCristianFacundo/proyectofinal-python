from django.contrib import admin
from .models import Cliente, Servicio, Presupuesto, Colaborador, Avatar

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Servicio)
admin.site.register(Presupuesto)
admin.site.register(Colaborador)
admin.site.register(Avatar)
