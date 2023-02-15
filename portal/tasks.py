from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from mmorpg import settings
from .models import Advert, User


# Отправляем автору объявления сообщение о новом отклике
@shared_task
def notify_new_response(instance):
    subscribers = Advert.objects.filter(id = instance.advert_id).values_list('author_id__email', flat=True)
    template = 'email_response_created.html'
    link = f'{settings.SITE_URL}/my_responses/'
    subject = 'Вы получили новый отклик'
    send_notification(instance, link, template, subject, subscribers)


# Отправляем сообщение автору отклика о том, что он был принят
@shared_task
def notify_response_accepted(instance):
    subscriber = User.objects.filter(id = instance.author_id).values_list('email', flat=True)
    link = f'{settings.SITE_URL}/my_responses/'
    template = 'email_response_accepted.html'
    subject = 'Ваш отклик был принят'
    send_notification(instance, link, template, subject, subscriber)

# Отправляем сообщение подписчикам о новом объявлении
@shared_task
def notify_new_advert(instance, pk):
    subscriber: list[str] = []
    subscriber += instance.advert_category.subscribers.all()
    subscriber = [s.email for s in subscriber]
    template = 'email_new_advert.html'
    link = f'{settings.SITE_URL}/{instance.pk}'
    subject = 'Новая статья по вашей подписке'
    send_notification(instance, link, template, subject, subscriber)


def send_notification(instance, link, template, subject, subscribers):
    html_content = render_to_string(
        template,
        {
            'instance': instance,
            'link': link
        }
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email='skilltests77@yandex.ru',
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()