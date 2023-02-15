from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Advert, Response, Category
from .forms import AdvertForm, ResponseForm
from .filters import ResponseFilter
from .tasks import notify_new_response, notify_response_accepted, notify_new_advert


class AdvertList(ListView):
    model = Advert
    ordering = '-advert_date'
    template_name = 'portal.html'
    context_object_name = 'adverts'
    paginate_by = 4


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'advert_detail.html'
    context_object_name = 'adv_detail'


class MyAdvertListView(ListView):
    model = Advert
    template_name = 'my_advert_list.html'
    context_object_name = 'my_advert_list'
    ordering = '-advert_date'
    paginate_by = 4

    def get_queryset(self):
        self.author_id = self.request.user.id
        queryset = Advert.objects.filter(author_id = self.author_id)
        return queryset


class AdvertCreate(LoginRequiredMixin, CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'advert_create.html'
    permission_required = ('portal.add_advert')

    def form_valid(self, form):
        adv = form.save(commit=False)
        form.instance.author_id = self.request.user.id
        adv.save()
        notify_new_advert(adv, adv.id)
        return super(AdvertCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('my_advert_list')


class AdvertUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'advert_create.html'
    context_object_name = 'adv_update'
    permission_required = ('portal.change_advert')


class AdvertDelete(LoginRequiredMixin, DeleteView):
    model = Advert
    template_name = 'advert_delete.html'
    success_url = reverse_lazy('advert_list')
    permission_required = ('portal.delete_advert')


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'
    context_object_name = 'adv_detail'
    permission_required = ('portal.add_response')

    def form_valid(self, form):
        resp = form.save(commit=False)
        form.instance.author_id = self.request.user.id
        form.instance.advert_id = self.kwargs.get('pk')
        notify_new_response(resp)
        return super(ResponseCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('advert_list')


class MyResponsesListView(FilterView):
    model = Response
    template_name = 'my_response_list.html'
    context_object_name = 'my_responses'
    filterset_class = ResponseFilter
    ordering = '-response_date'
    paginate_by = 4

    def get_queryset(self):
        self.author_id = self.request.user.id
        queryset = Response.objects.filter(advert__author_id=self.author_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Принимаем отклик и отправляем автору сообщение о этом
def response_accept(request, pk):
    resp = Response.objects.get(id = pk)
    resp.response_accepted = True
    resp.save(update_fields = ['response_accepted'])
    notify_response_accepted(resp)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Удаляем отклик
def response_delete(request, pk):
    resp = Response.objects.get(id = pk)
    resp.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Подписка текущего пользователя на категорию
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




