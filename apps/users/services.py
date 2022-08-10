from django.conf import settings
from django.core.mail import send_mail


def send_email_to_user(email, message):
    send_mail(
        'Здравствуйте! Вас приветствует компания Flex Team!',
        message,
        settings.EMAIL_HOST_USER,
        [email, ],
        fail_silently=False
    )
