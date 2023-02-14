from django.db import models
from django.http import HttpResponseRedirect, request, response
from django.urls import reverse
from django.contrib.auth.models import User

class Advert(models.Model):

    tanks = 'TK'
    heals = 'HL'
    DD = 'DD'
    dealers = 'DL'
    guildmasters = 'GM'
    questgivers = 'QG'
    blacksmiths = 'BS'
    tanners = 'TN'
    potion_master = 'PM'
    spell_master = 'SM'

    TYPE_CHOICES = [
        (tanks, 'Танки'),
        (heals, 'Хилы'),
        (DD, 'ДД'),
        (dealers, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_master, 'Зельевар'),
        (spell_master, 'Мастер заклинаний')

    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    advert_date = models.DateTimeField(auto_now_add=True)
    advert_category = models.CharField(max_length=2, choices=TYPE_CHOICES, default='TK')
    advert_title = models.CharField(max_length=255)
    advert_text = models.TextField()

    def __str__(self):
        return f'{self.advert_title}'

    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.id)])


class Response(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='advert_responses')
    response_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    response_accepted = models.BooleanField(default=False)
    response_date = models.DateTimeField(auto_now_add=True)

    def response_accept(self):
        idr = self.id
        resp = Response.objects.get(id = idr)
        resp.response_accepted = True
        resp.save()
        # return HttpResponseRedirect(response.META['HTTP_REFERER'])

    def get_absolute_url(self):
        return reverse('my_response_list')

