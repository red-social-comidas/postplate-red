from django.contrib import admin
from .models import Publication, Files 

# Registra el modelo "Files" en el admin
@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('file',)  # Muestra el campo 'file' en la lista del admin

# Registra el modelo "Publication" en el admin
@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'publication_date', 'content')  # Campos que deseas mostrar
    list_filter = ('publication_date', 'id_user')  # Filtros que deseas usar
    search_fields = ('content',)  # Campo que puedes buscar
