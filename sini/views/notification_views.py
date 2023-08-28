from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from ..models import Notification
from ..forms import NotificationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
import json 
from django.shortcuts import render, redirect, get_object_or_404

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'sini/notification/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(NotificationListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['sini','notification']
        context['active_menu'] ='appmobile'

    


        if 'subject' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True

        
        self.request.session['page_from'] = ""
        self.request.session['referer'] = {}

        context['value_subject'] = self.request.GET.get('subject', '')

        if context['is_paginated']:
            list_pages = []

            if 'subject' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(NotificationListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(NotificationListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(NotificationListView.get_queryset(self)) / self.paginate_by) + 1

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
        query = {'subject': self.request.GET.get('subject', None)}

        query_result =  Notification.objects.order_by('-created')


        if query['subject'] and query['subject'] != '':
            query_result = query_result.filter(subject__icontains=query['subject'])

  
        return query_result
    


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'notification'
    template_name = 'sini/notification/notification_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini','notification']
        context['active_menu'] ='appmobile'
        
        return context
    


class NotificationCreateView(LoginRequiredMixin, CreateView):
    model = Notification
    context_object_name = 'notification'
    template_name = 'sini/notification/notification_form.html'
    form_class = NotificationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ['sini', 'notification']
        context['active_menu'] = 'appmobile'

        return context

    def get_success_url(self):
        return reverse_lazy("sini:notification_list", kwargs={})

    def form_valid(self, form):
        notification = form.save(commit=False)
        notification.created_by = self.request.user  # use your own profile here
        notification.save()
        return super(NotificationCreateView, self).form_valid(form)

