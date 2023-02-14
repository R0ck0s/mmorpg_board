from django_filters import ModelChoiceFilter, FilterSet
from .models import Advert, Response

def get_adverts_quertyset(request):
    queryset = Advert.objects.filter(author_id=request.user)
    return queryset


class ResponseFilter(FilterSet):
    advert = ModelChoiceFilter(queryset=get_adverts_quertyset, label='Мои объявления', empty_label='Все объявления')

    class Meta:
        model = Advert
        fields =["advert"]



