import cloudinary.uploader

from rest_framework import serializers
from .models import Files, Publication


# Define un serializer para el modelo "Files" que gestiona los archivos adjuntos.
class FilesSerializer(serializers.ModelSerializer):
    file_public_id = serializers.CharField(read_only=True)

    class Meta:
        model = Files
        fields = ['id', 'file', 'file_public_id']


# Define un serializer para el modelo "Publication" que gestiona las publicaciones.
class PublicationSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    file_public_id = serializers.CharField(read_only=True)
    files_set = FilesSerializer(many=True, read_only=True)
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Publication
        fields = ['id', 'content', 'publication_date',
                  'files', 'files_set', 'file_public_id', 'id_user']

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        publication = Publication.objects.create(**validated_data)

        for file_data in files_data:
            # Subir a Cloudinary y obtener la URL segura
            upload_result = cloudinary.uploader.upload(
                file_data, resource_type="auto")
            Files.objects.create(
                publication=publication,
                file=upload_result['secure_url'],
                file_public_id=upload_result['public_id']
            )

        return publication
