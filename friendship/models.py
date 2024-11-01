from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Definición de los posibles estados de una solicitud de amistad
# 'pending': la solicitud está en espera de respuesta
# 'accepted': la solicitud ha sido aceptada
# 'declined': la solicitud ha sido rechazada
states = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('declined', 'Declined'),
]


class Friends(models.Model):
    # id_user1 es el usuario que envía la solicitud de amistad.
    # 'related_name' define cómo acceder a las solicitudes desde el modelo 'CustomUser'.
    id_user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friends_set1')

    # id_user2 es el usuario que recibe la solicitud de amistad.
    id_user2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friends_set2')

    # Campo que almacena el estado de la solicitud, utilizando los valores de la lista 'states'.
    # El estado por defecto es 'pending' (solicitud en espera).
    state = models.CharField(
        max_length=10, choices=states, default='pending')

    # Fecha en la que se envía la solicitud de amistad, se establece automáticamente al crear la instancia.
    application_date = models.DateTimeField(auto_now_add=True)

    # Fecha en la que se acepta la solicitud de amistad, inicialmente es null porque no está aceptada al inicio.
    acceptance_date = models.DateTimeField(null=True, blank=True)

    # Fecha en la que se rechaza la solicitud de amistad, inicialmente es null porque no está rechazada al inicio.
    rejection_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Establece una restricción única para evitar duplicados.
        # Un usuario no puede enviar múltiples solicitudes de amistad al mismo usuario.
        constraints = [
            models.UniqueConstraint(
                fields=['id_user1', 'id_user2'], name='unique_friendship')
        ]

    # Método para aceptar la solicitud de amistad.
    # Cambia el estado a 'accepted' y registra la fecha de aceptación.
    def accept(self):
        self.state = 'accepted'
        # Guarda la fecha y hora actuales.
        self.acceptance_date = timezone.now()
        self.save()  # Guarda los cambios en la base de datos.

    # Método para rechazar la solicitud de amistad.
    # Cambia el estado a 'declined' y registra la fecha de rechazo.
    def decline(self):
        self.state = 'declined'
        # Guarda la fecha y hora actuales.
        self.rejection_date = timezone.now()
        self.save()  # Guarda los cambios en la base de datos.
