from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import AuditoriaAcceso

@receiver(user_logged_in)
def registrar_acceso(sender, user, request, **kwargs):
    print(f"Señal user_logged_in recibida para el usuario: {user.username}") # DEBUG
    AuditoriaAcceso.objects.create(
        usuario=user,
        accion="Inicio de sesión"
    )
    print("Registro de AuditoriaAcceso creado.") # DEBUG