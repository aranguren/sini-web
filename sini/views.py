from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.conf import settings

from .tokens import account_activation_token  
from django.core.mail import EmailMessage  


from .models import Incidence, ApiUser, ApiGroup
from .forms import ApiUserForm

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
        context['value_email'] = self.request.GET.get('email', '')

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

        

        query_result =  Incidence.objects.order_by('-created')


        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])
        if query['codigo'] and query['codigo'] != '':
            query_result = query_result.filter(codigo__icontains=query['codigo'])
  

        return query_result




def create_api_user(request):
    """Vista que crea un usuario api y envia un correo con los datos para activar la cuenta"""

    val_errors=[]


    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ApiUserForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
     

            name = form.cleaned_data['name']
            #nombre = form.cleaned_data['nombre'] or "Vacio"
            #apellidos= form.cleaned_data['apellidos'] or ""
            email= form.cleaned_data['email']
            group = form.cleaned_data['geoup']


            username_exists = ApiUser.objects.filter(email=email)
            if username_exists:
                val_errors.append("Ya existe un usuario con el mismo correo electrónico, favor intente con otro o bien contáctese con el administrador del sistema")    
                
                context = {
                    'form': form,                          
                    'val_errors':val_errors,
                }

                return render(request, 'agrimensuras/topografo_form.html', context)
            
            api_group = ApiGroup.objects.get(id=int(group))
            new_user = ApiUser(name=name,email=email, group=api_group)#, first_name=nombre, last_name=apellidos)
            new_user.active = False 

            new_user.save()  

            current_site = get_current_site(request) #"localhost:8000" #get_current_site(request)  
            mail_subject = 'Enlace para activación de cuenta en INETER'  
            uid = urlsafe_base64_encode(force_bytes(new_user.id))

            token = account_activation_token.make_token(new_user)

            uiddecoded = force_text(urlsafe_base64_decode(uid))  
            new_user.save() 
            message = render_to_string('agrimensuras/acc_active_email.html', {  
                'user': new_user,  
                'domain': current_site.domain,  
                'uid':uid,  
                'token':token,  
            })  
            
            email_message = EmailMessage(  
                        mail_subject, message, to=[email], from_email= settings.DEFAULT_FROM_EMAIL # "idec@deneb.io"  
            )  
            email_message.content_subtype = "html"  
            email_message.send()  


                
            # to get the domain of the current site  
            current_site = get_current_site(request) #"localhost:8000" #get_current_site(request)  
            mail_subject = 'Enlace para activación de cuenta en INETER'  
            uid = urlsafe_base64_encode(force_bytes(new_user.id))

            token = account_activation_token.make_token(new_user)

            uiddecoded = force_text(urlsafe_base64_decode(uid))  
            new_user.save() 
            message = render_to_string('agrimensuras/acc_active_email.html', {  
                'user': new_user,  
                'domain': current_site.domain,  
                'uid':uid,  
                'token':token,  
            })  
            
            email_message = EmailMessage(  
                        mail_subject, message, to=[email], from_email= settings.DEFAULT_FROM_EMAIL # "idec@deneb.io"  
            )  
            email_message.content_subtype = "html"  
            email_message.send()  


            # aqui se hara el acceso al api y se obtendran los valores
       


# If this is a GET (or any other method) create the default form.
    else:
        form = ApiUserForm()


    context = {
        'form': form,
        'val_errors':val_errors,

    }

    return render(request, 'agrimensuras/topografo_form.html', context)
