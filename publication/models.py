import cloudinary
import cloudinary.uploader
import cloudinary.models

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Importa el modelo de usuario predeterminado del sistema, que es usado para gestionar a los usuarios registrados.
CustomUser = get_user_model()


def blog_thumbnail_directory(instance, filename=None):
    """
    Define la ruta de la carpeta en Cloudinary donde se subirá el archivo, 
    organizando en carpetas según el nombre del usuario y el tipo de archivo (imagen o video).
    """
    if not filename:
        filename = instance.name if hasattr(instance, 'name') else 'untitled'

    user_name = instance.publication.id_user.username if hasattr(
        instance, 'publication') else 'unknown'

    ext = filename.split('.')[-1].lower()

    folder = 'imagenes' if ext in ['jpg', 'jpeg', 'png', 'gif'] else \
             'videos' if ext in ['mp4', 'mov', 'avi', 'mkv'] else 'otros'

    return f'publications/{user_name}/{folder}/{filename}'


# Define el modelo "Publication" que representa una publicación en la aplicación.
class Publication(models.Model):
    # Relaciona cada publicación con un usuario (autor). Si el usuario es eliminado, sus publicaciones también se eliminan (on_delete=models.CASCADE).
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Campo que almacena el contenido de la publicación (como texto).
    content = models.TextField()

    # Guarda la fecha y hora en la que la publicación se creó automáticamente.
    publication_date = models.DateTimeField(auto_now_add=True)

    # Método para validar que una publicación no tenga más de 10 archivos adjuntos.
    def clean(self):
        if self.files_set.count() > 10:
            # Lanza un error si se intenta añadir más de 10 archivos.
            raise ValidationError("No more than 10 files are allowed.")

    def delete(self, *args, **kwargs):
        for file in self.files_set.all():
            if file.file_public_id:
                cloudinary.uploader.destroy(file.file_public_id)
        super().delete(*args, **kwargs)


# Define el modelo "Files" que representa los archivos adjuntos a una publicación (como imágenes o videos).
class Files(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name='files_set')

    # Cambia el campo FileField por CloudinaryField para almacenar los archivos en Cloudinary.
    file = models.URLField(max_length=500)
    file_public_id = models.CharField(max_length=100, blank=True, null=True)
