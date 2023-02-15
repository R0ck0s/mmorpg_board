from django_summernote.admin import SummernoteModelAdmin

from django.contrib import admin

from .models import Advert


class AdvertAdmin(SummernoteModelAdmin):
    list_display = ('advert_title', 'author', 'advert_date')
    search_fields = ('advert_title', 'advert_text')
    summernote_fields = ('advert_text')


admin.site.register(Advert, AdvertAdmin)

