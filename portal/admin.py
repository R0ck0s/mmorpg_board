from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Advert


class AdvertAdmin(SummernoteModelAdmin):
    list_display = ('advert_title', 'author', 'advert_category', 'advert_date')
    search_fields = ('advert_title', 'advert_text')
    summernote_fields = ('advert_text')

# Register your models here.

admin.site.register(Advert, AdvertAdmin)

