from portal.models import Advert, Response


def response_count(request):

    resp = Response.objects.filter(advert__author_id = request.user.id).count()
    return {"var": resp}