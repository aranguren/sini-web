from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Incidence

class IncidenciaListView(LoginRequiredMixin, ListView):
    model = Incidence
    template_name = 'ganaclima/farm/farm_list.html'
    context_object_name = 'farms'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(IncidenciaListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['ganaclima','finca']
        context['active_menu'] ='ganaclima'

    
        context['value_name'] = self.request.GET.get('name', '')
        context['value_codigo'] = self.request.GET.get('codigo', '')

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

                if len(IncidenciaListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(IncidenciaListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(IncidenciaListView.get_queryset(self)) / self.paginate_by) + 1

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
        query = {'name': self.request.GET.get('name', None),
                 'codigo': self.request.GET.get('codigo', None)}

        

        query_result =  Incidence.objects.order_by('name')


        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])
        if query['codigo'] and query['codigo'] != '':
            query_result = query_result.filter(codigo__icontains=query['codigo'])
  

        return query_result
