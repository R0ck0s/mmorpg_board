from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from .models import Advert, User

from django.template.loader import render_to_string


@shared_task
def notify_new_response(instance):
    subscriber = Advert.objects.filter(id = instance.advert_id).values_list('author_id__email', flat=True)[0]
    html_content = render_to_string(
        'email_response_created.html',
        {
            'response': instance,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Вы получили новый отклик',
        body='',
        from_email='skilltests77@yandex.ru',
        to=[subscriber],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def notify_response_accepted(instance):
    subscriber = User.objects.filter(id = instance.author_id).values_list('email', flat=True)[0]
    html_content = render_to_string(
        'email_response_accepted.html',
        {
            'response': instance,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Ваш отклик был принят',
        body='',
        from_email='skilltests77@yandex.ru',
        to=[subscriber],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()