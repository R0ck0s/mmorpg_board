from django.urls import path
from .views import AdvertList, AdvertDetail, AdvertCreate, AdvertUpdate, AdvertDelete, ResponseCreate, \
    MyAdvertListView, MyResponsesListView, response_accept, response_delete, subscribe

urlpatterns = [
    path('', AdvertList.as_view(), name='advert_list'),
    path('<int:pk>', AdvertDetail.as_view(), name='advert_detail'),
    path('create/', AdvertCreate.as_view(), name='advert_create'),
    path('<int:pk>/update/', AdvertUpdate.as_view(), name='adv_update'),
    path('<int:pk>/delete/', AdvertDelete.as_view(), name='adv_delete'),
    path('<int:pk>/response/', ResponseCreate.as_view(), name='resp_create'),
    path('my_adverts/', MyAdvertListView.as_view(), name='my_advert_list'),
    path('my_responses/', MyResponsesListView.as_view(), name='my_response_list'),
    path('my_responses/accept/<int:pk>/', response_accept, name='accept'),
    path('my_responses/delete/<int:pk>/', response_delete, name='resp_delete'),
    path('subscribe/<int:pk>/', subscribe, name='subscribe'),

]