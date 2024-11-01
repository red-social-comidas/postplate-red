import base64
import six
import uuid
import imghdr
import cloudinary.uploader

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

CustomUser = get_user_model()


class UserEmailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)
    role = serializers.CharField(source='get_role', read_only=True)
    images = serializers.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2',
                  'first_name', 'last_name', 'images', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email is already in use."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        image_file = validated_data.pop('images', None)
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder=f'blog_thumbnails/{validated_data["username"]}'
            )
            image_url = upload_result['secure_url']
            image_public_id = upload_result['public_id']
        else:
            image_url = None
            image_public_id = None

        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            images=image_url,
            image_public_id=image_public_id
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('email', 'password')

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.")
        return data


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        # Si es "null" o None, retornar None
        if data == "null" or data is None:
            return None

        # Si es un archivo, retornar el archivo
        if hasattr(data, 'file'):
            return data

        raise serializers.ValidationError("Tipo de dato inválido para imagen")


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role', read_only=True)
    images = CustomImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'images', 'verified', 'date_joined', 'role')

    def update(self, instance, validated_data):
        try:
            # Verificar si 'images' está en validated_data
            if 'images' in validated_data:
                image_value = validated_data.pop('images')

                # Si hay una imagen existente y se recibió None, eliminarla
                if image_value is None:
                    if instance.image_public_id:
                        try:
                            cloudinary.uploader.destroy(
                                instance.image_public_id)
                        except Exception as e:
                            print(
                                f"Error al eliminar imagen anterior: {str(e)}")

                    instance.images = None
                    instance.image_public_id = None

                # Si se envió un archivo
                elif image_value:
                    # Eliminar imagen anterior si existe
                    if instance.image_public_id:
                        try:
                            cloudinary.uploader.destroy(
                                instance.image_public_id)
                        except Exception as e:
                            print(
                                f"Error al eliminar imagen anterior: {str(e)}")

                    # Subir nueva imagen
                    upload_result = cloudinary.uploader.upload(
                        image_value,
                        folder=f'blog_thumbnails/{instance.username}',
                        resource_type='auto'
                    )
                    instance.images = upload_result['secure_url']
                    instance.image_public_id = upload_result['public_id']

            # Actualizar otros campos
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance

        except Exception as e:
            raise serializers.ValidationError(
                f"Error al procesar la imagen: {str(e)}")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['images'] = instance.images if instance.images else None
        return data
