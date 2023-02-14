from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea
from django_summernote.widgets import SummernoteWidget

from .models import Advert, Response



class AdvertForm(forms.ModelForm):
    class Meta:
       model = Advert
       fields = [
           'advert_category',
           'advert_title',
           'advert_text',
       ]
       labels = {
           'advert_category': 'Категория',
           'advert_title': 'Заголовок',
           'advert_text': 'Описание',
       }
       widgets = {
            'advert_text': SummernoteWidget,
       }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('advert_title')
        text = cleaned_data.get('advert_text')

        if text == title:
            raise ValidationError(
                {'text': 'Текст публикации не должен быть идентичен её названию'}
            )
        return cleaned_data

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            # 'author',
            'response_text',
        ]
        labels = {
            'response_text': '',
        }
        widgets = {
            'response_text': Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder': 'Введтие текст отклика'}),
        }
