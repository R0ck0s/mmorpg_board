from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Advert, Response
from .forms import AdvertForm, ResponseForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ResponseFilter
from django_filters.views import FilterView
from .tasks import notify_new_response, notify_response_accepted


class AdvertList(ListView):
    model = Advert
    ordering = 'advert_date'
    template_name = 'portal.html'
    context_object_name = 'adverts'
    paginate_by = 4

class AdvertDetail(DetailView):
    model = Advert
    template_name = 'advert_detail.html'
    context_object_name = 'adv_detail'

class AdvertCreate(LoginRequiredMixin, CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'advert_create.html'
    permission_required = ('portal.add_advert')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
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


class MyAdvertListView(ListView):
    model = Advert
    template_name = 'my_advert_list.html'
    context_object_name = 'my_advert_list'
    paginate_by = 4

    def get_queryset(self):
        self.author_id = self.request.user.id
        queryset = Advert.objects.filter(author_id = self.author_id)
        return queryset

class MyResponsesListView(FilterView):
    model = Response
    template_name = 'my_response_list.html'
    context_object_name = 'my_responses'
    filterset_class = ResponseFilter
    paginate_by = 4

    def get_queryset(self):
        self.author_id = self.request.user.id
        queryset = Response.objects.filter(advert__author_id=self.author_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def response_accept(request, pk):
    resp = Response.objects.get(id = pk)
    resp.response_accepted = True
    resp.save(update_fields = ['response_accepted'])
    notify_response_accepted(resp)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def response_delete(request, pk):
    resp = Response.objects.get(id = pk)
    resp.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




# def response_accept(self):
#     self.response.response_accepted = True
#     response.save(update_fields=['response_accepted'])
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#     message = 'Вы успешно подписались на рассылку новостей категории'
#     return render(request, 'post_created_email.html', {'category': category, 'message': message})

# def upgrade_user(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors_group.user_set.add(user)
#         Author.objects.create(user_id=user.id)
#     return redirect('/my_responses/')



