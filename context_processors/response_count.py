from portal.models import Response

# Контекстный процессор, который передаёт количество откликов текущего пользователя в базовый шаблон
def response_count(request):
    resp = Response.objects.filter(advert__author_id = request.user.id).count()
    return {"var": resp}