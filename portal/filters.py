from django_filters import ModelChoiceFilter, FilterSet
from .models import Advert, Response

# Получаем queryset с объявлениями текущего юзера
def get_adverts_quertyset(request):
    queryset = Advert.objects.filter(author_id=request.user)
    return queryset


# Фильтруем мои отклики по объявлениям для шаблона "my_response_list.html"
class ResponseFilter(FilterSet):
    advert = ModelChoiceFilter(queryset=get_adverts_quertyset, label='Мои объявления', empty_label='Все объявления')

    class Meta:
        model = Advert
        fields =["advert"]



