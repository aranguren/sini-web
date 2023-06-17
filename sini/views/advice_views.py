from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from ..models import Advice
from ..forms import AdviceForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
import json 




class AdviceListView(LoginRequiredMixin, ListView):
    model = Advice
    template_name = 'sini/advice/advice_list.html'
    context_object_name = 'advices'
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(AdviceListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['sini','advice']
        context['active_menu'] ='sini'

    


        if 'name' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True

        
        self.request.session['page_from'] = ""
        self.request.session['referer'] = {}

        if context['is_paginated']:
            list_pages = []

            if 'name' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(AdviceListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(AdviceListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(AdviceListView.get_queryset(self)) / self.paginate_by) + 1

                if paginated > 1:
                    for i in range(int(first_range), int(first_range) + 5):
                        if i <= paginated:
                            list_pages.append(i)

                    context['total_pages'] = paginated
                    context['has_more_pages'] = True if int(first_range) < paginated else False
                    context['next_page'] = int(first_range) + 1 if int(first_range) < paginated else '0'
                    context['has_previous_pages'] = True if int(first_range) > 1 else False
                    context['previous_page'] = int(first_range) - 1 if int(first_range) > 1 else '0'
                    context['actual_page'] = int(first_range)

            context['paginator_rows'] = list_pages

        return context

    def get_queryset(self):
        query = {'name': self.request.GET.get('name', None)}

        query_result =  Advice.objects.order_by('name')


        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])

  
        return query_result
    


class AdviceDetailView(LoginRequiredMixin, DetailView):
    model = Advice
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'advice'
    template_name = 'sini/advice/advice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini','advice']
        context['active_menu'] ='sini'
        
        return context


class AdviceCreateView(LoginRequiredMixin, CreateView):
    model = Advice
    context_object_name = 'advice'
    template_name = 'sini/advice/advice_form.html'
    form_class = AdviceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ['sini', 'advice']
        context['active_menu'] = 'sini'

        return context

    def get_success_url(self):
        return reverse_lazy("sini:advice_detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        warning = form.save(commit=False)
        warning.created_by = self.request.user  # use your own profile here
        warning.save()
        return super(AdviceCreateView, self).form_valid(form)


class AdviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Advice
    context_object_name = 'advice'
    template_name = 'sini/advice/advice_form.html'
    form_class = AdviceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ['sini', 'advice']
        context['active_menu'] = 'sini'

        return context

    def get_success_url(self):
        return reverse_lazy("sini:advice_detail", kwargs={"pk": self.object.id})


    def form_valid(self, form):
        api_user = form.save(commit=False)
        api_user.modified_by = self.request.user 
        return super(AdviceUpdateView, self).form_valid(form)
    



@login_required(login_url='/login/')
def advice_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id = query['id']
    print(id)
   
    advice = Advice.objects.get(id=id)
    #raise RestrictedError("Debe eliminar primero el bla bla ", warning)
    try:
        advice.delete()
    except RestrictedError as e:
        resp['mensaje'] = 'restricted'
        resp['error'] = "{} {}".format(e.args[0], str(e.args[1]))
        return JsonResponse(resp, status=500)
    except Exception as e:
        resp['mensaje'] = 'error'
        resp['error'] = json.dumps(e)
        return JsonResponse(resp, status=500)

    resp['mensaje'] = 'deleted'
    print(resp)
    return JsonResponse(resp, status=200)
