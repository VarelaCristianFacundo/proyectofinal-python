# Tercera Pre-Entrega - Cristian Facundo Varela

## Proyecto CoderHouse Django 🚀

_Este proyecto simula un sistema de gestión de presupuestos para una empresa de servicios lingüísticos._

## Instrucciones de Uso

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:

**1. Clona el repositorio en tu máquina local.**

**2. Abre una terminal en la raíz del proyecto.**

**3. Crea y activa un entorno virtual:**

```bash
python -m venv nombre_del_entorno
En Windows: .\\nombre_del_entorno\\Scripts\\activate
En Linux/Mac: source ./nombre_del_entorno/bin/activate
```

**4. Instala las dependencias del proyecto:**

```bash
pip install -r requirements.txt
```

**5. Navega hasta la carpeta del proyecto:**

```bash
cd proyectofinal
```

**6. Ejecuta las migraciones de Django:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**7. Inicia el servidor:**

```bash
python manage.py runserver
```

**8. Abre un navegador y accede a http://127.0.0.1:8000/App/ para ver la página principal.**

## Funcionalidades Principales

_El sitio web proporciona las siguientes funcionalidades:_

- Home: Página de inicio.

- Presupuesto: Permite agregar un nuevo presupuesto.

- Lista de Presupuestos: Ofrece la posibilidad de buscar, editar y eliminar presupuestos existentes. También incluye un botón "Crear un nuevo Presupuesto" que te lleva al formulario de creación.

- Lista de Colaboradores: Muestra los colaboradores de la empresa y permite asignarles presupuestos para su ejecución. Un presupuesto solo se puede asignar una vez a cada colaborador para evitar duplicaciones.

- Proyectos Asignados: Permite visualizar los proyectos asignados a cada colaborador.

- Acceso al Administrador:
  Para acceder al panel de administración de la página, dirígete a http://127.0.0.1:8000/admin. Los datos de acceso son:

- _Usuario: "cvarela"_
- _Contraseña: "never123"_
