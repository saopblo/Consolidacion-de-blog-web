# Blog Django

Aplicación web de blog desarrollada con Django. Permite publicar artículos con imágenes, administrar perfiles y avatares, y comentar publicaciones.

## Funcionalidades

- **Publicaciones:** crear, consultar, editar y eliminar posts desde la web. Cada post puede incluir una imagen y tiene un enlace basado en su slug.
- **Estados y visibilidad:**
  - Los posts publicados son visibles para cualquier visitante.
  - Los borradores y los posts archivados solo son visibles para su autor, incluso si otro usuario inició sesión.
  - Cada usuario puede crear posts, pero solo el autor puede editar, ver si no está publicado, o eliminar su propio contenido.
- **Comentarios:** solo usuarios autenticados pueden agregar comentarios. Los visitantes anónimos pueden leer los comentarios de las publicaciones que tienen permitido ver.
- **Cuentas y perfiles:** registro, inicio y cierre de sesión, edición del perfil y carga de avatar. Las opciones de perfil y avatar están agrupadas en el menú del usuario autenticado. El avatar se muestra dentro de un espacio de dimensiones definidas y se adapta sin recortar la imagen.
- **Permisos:** crear publicaciones, comentar, editar el perfil y cargar un avatar requiere iniciar sesión. Las rutas de edición y eliminación también verifican que el usuario sea el autor.
- **Confirmaciones:** la eliminación de un post muestra una pantalla para confirmar o cancelar antes de borrarlo. Al elegir cerrar sesión, el sitio solicita confirmación.
- **Búsqueda:** permite buscar publicaciones por título, contenido, autor y fecha.

## Tecnologías

- Python 3.12 o posterior
- Django 6.1.1
- SQLite
- Pillow para el manejo de imágenes
- python-decouple para la configuración
- Plantillas Django, HTML, CSS y Bootstrap

## Requisitos

- Python 3.12 o posterior
- Git

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/saopblo/Pre_entrega_10.git
cd Pre_entrega_10
```

### 2. Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar el entorno local

Crea un archivo `.env` a partir de `.env.example`.

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

En macOS o Linux:

```bash
cp .env.example .env
```

Revisa el archivo `.env` y configura `SECRET_KEY` con una clave local propia. `DEBUG=True` sirve para desarrollo local; no uses el modo de depuración ni claves de desarrollo en producción. El archivo `.env` está excluido de Git.

### 5. Crear la base de datos

Aplica las migraciones incluidas en el repositorio:

```bash
python manage.py migrate
```

### 6. Crear una cuenta

Inicia el servidor y registra un usuario desde la opción **Registrarse**. Para probar el panel de administración, crea además un superusuario:

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Abre <http://127.0.0.1:8000/> en el navegador. El panel de administración está disponible en <http://127.0.0.1:8000/admin/>.

## Imágenes y archivos estáticos

Los archivos estáticos de la interfaz están dentro de `posts/static/`. Las imágenes cargadas para posts y avatares se guardan localmente bajo `media/`; esa carpeta y la base de datos local `db.sqlite3` están excluidas de Git. Al configurar el proyecto desde cero, la base de datos se crea con `migrate` y las imágenes se pueden cargar desde la aplicación.

## Cuentas para pruebas

No se publican contraseñas ni credenciales compartidas en este repositorio. Para probar el sitio, registra una cuenta propia desde la web. Si necesitas acceder al admin, crea un superusuario local con `python manage.py createsuperuser`.

## Autor

Pablo Nuñez
