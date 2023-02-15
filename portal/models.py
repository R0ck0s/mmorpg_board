from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.category_name}'


class Advert(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    advert_date = models.DateTimeField(auto_now_add=True)
    advert_category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
        resp = Response.objects.get(id = self.id)
        resp.response_accepted = True
        resp.save()

    def get_absolute_url(self):
        return reverse('my_response_list')

