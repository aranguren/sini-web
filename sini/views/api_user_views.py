from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404, get_list_or_404,  redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from passlib.hash import pbkdf2_sha256 as sha256
from django.db.models import RestrictedError
from ..tokens import account_activation_token  
from django.core.mail import EmailMessage  


from ..models import ApiUser, ApiGroup
from ..forms import ApiUserForm

class ApiUserListView(LoginRequiredMixin, ListView):
    model = ApiUser
    template_name = 'sini/api_user/api_user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(ApiUserListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['appmobile','api_user']
        context['active_menu'] ='appmobile'

    
        context['value_name'] = self.request.GET.get('name', '')
        context['value_codigo'] = self.request.GET.get('codigo', '')

        if 'name' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True

        
        self.request.session['page_from'] = ""
        self.request.session['referer'] = {}

        groups = ApiGroup.objects.all()
        context['groups'] = groups

        context['value_name'] = self.request.GET.get('name', '')
        context['value_email'] = self.request.GET.get('email', '')
        context['value_group'] = self.request.GET.get('group', '')
        context['value_active'] = self.request.GET.get('active', '')

        if context['is_paginated']:
            list_pages = []

            if 'name' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(ApiUserListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(ApiUserListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(ApiUserListView.get_queryset(self)) / self.paginate_by) + 1

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
                 'email': self.request.GET.get('email', None),
                 'group': self.request.GET.get('group', None),
                 'active': self.request.GET.get('active', None),
                 
                 }

        query_result =  ApiUser.objects.order_by('name')

        if query['active'] and query['active'] != '':
            if query['active']=='si':
                query_result = query_result.filter(active=True)
            elif query['active']=='no':
                query_result = query_result.filter(active=False)
            elif query['active']=='si_no':
                pass


        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])
        if query['email'] and query['email'] != '':
            query_result = query_result.filter(email__icontains=query['email'])
        if query['group'] and query['group'] != '':
            group_id = int(query['group'])
            group = ApiGroup.objects.get(id=group_id)
            query_result = query_result.filter(group=group )
  
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
            group = form.cleaned_data['group']
         


            username_exists = ApiUser.objects.filter(email=email)
            if username_exists:
                val_errors.append("Ya existe un usuario con el mismo correo electrónico, favor intente con otro o bien contáctese con el administrador del sistema")    
                
                context = {
                    'form': form,                          
                    'val_errors':val_errors,
                }
                context['segment'] = ['appmobile','api_user']
                context['active_menu'] ='appmobile'
                return render(request, 'sini/api_user/api_user_form.html', context)
            
            #api_group = ApiGroup.objects.get(id=int(group))
            new_user = ApiUser(name=name,email=email, group=group)#, first_name=nombre, last_name=apellidos)
            new_user.active = False 

            User = get_user_model()
            password_random = User.objects.make_random_password() # 7Gjk2kd4T9

            password = sha256.hash(password_random)
            new_user.password = password

            new_user.save()  

            current_site = get_current_site(request) #"localhost:8000" #get_current_site(request)  
            mail_subject = 'Enlace para activación de cuenta en AlertaDo'  
            uid = urlsafe_base64_encode(force_bytes(new_user.id))

            token = account_activation_token.make_token(new_user)

            uiddecoded = force_text(urlsafe_base64_decode(uid))  
      
            message = render_to_string('sini/api_user/acc_active_email.html', {  
                'user': new_user,  
                'domain': current_site.domain,  
                'uid':uid,  
                'token':token,  
                'email': new_user.email,
                'password_random':password_random
            })  
            
            email_message = EmailMessage(  
                        mail_subject, message, to=[email], from_email= settings.DEFAULT_FROM_EMAIL # "idec@deneb.io"  
            )  
            email_message.content_subtype = "html"  
            email_message.send()  

            redirect = reverse_lazy("sini:api_user_detail", kwargs={"pk":new_user.id})
  
            return HttpResponseRedirect(redirect)


# If this is a GET (or any other method) create the default form.
    else:
        form = ApiUserForm()


    context = {
        'form': form,
        'val_errors':val_errors,

    }
    context['segment'] = ['appmobile','api_user']
    context['active_menu'] ='appmobile'

    return render(request, 'sini/api_user/api_user_form.html', context)


class ApiUserDetailView(LoginRequiredMixin, DetailView):
    model = ApiUser
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'api_user'
    template_name = 'sini/api_user/api_user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['appmobile','api_user']
        context['active_menu'] ='appmobile'
        
        return context
    

    


class ApiUserUpdateView(LoginRequiredMixin, UpdateView):
    model = ApiUser
    context_object_name = 'api_user'
    template_name = 'sini/api_user/api_user_form.html'
    form_class = ApiUserForm
    
    def get_success_url(self):
        return reverse_lazy("sini:api_user_detail", kwargs={"pk":self.object.id})   

    def form_valid(self, form):
        api_user = form.save(commit=False)
        api_user.modified_by = self.request.user 
        return super(ApiUserUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['appmobile','api_user']
        context['active_menu'] ='appmobile'
        
        return context
    


def activate_user(request, uidb64, token):  
    #User = get_user_model()  
    context={}
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = ApiUser.objects.get(id=uid)  
    except(TypeError, ValueError, OverflowError ):
        context['status']='error'
        context['error'] = "invalid_token"
        user = None
    except ApiUser.DoesNotExist:
        context['status']='error'
        context['error'] = "user_not_found"
        user = None  
    except Exception as e:
        context['status']='error'
        context['error'] = "unknown"
        context['error_message']= str(e)
        user = None
    else: 
        if user is not None and not account_activation_token.check_token(user, token):
            context['status']='error'
            context['error'] = "invalid_token"
        elif user is not None and account_activation_token.check_token(user, token):  
             
            user.active = True  
            user.save()  
            #return HttpResponseRedirect(reverse("agrimensuras:topografo_activate"))
            context['api_user']=user
            context['status']='ok'
            return render(request, 'sini/api_user/api_user_activate.html', context)     


    return render(request, 'sini/api_user/api_user_activate.html', context)  


class ApiUserArchiveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        user = get_object_or_404(ApiUser, pk=pk)
        user.active = False
        user.save()
        redirection = reverse_lazy("sini:api_user_detail", kwargs={"pk": pk}) 
        return redirect(redirection)

class ApiUserActivateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        user = get_object_or_404(ApiUser, pk=pk)
        user.active = True
        user.save()
        redirection = reverse_lazy("sini:api_user_detail", kwargs={"pk": pk}) 
        return redirect(redirection)
    

    import time

@login_required(login_url='/login/')
def user_change_password(request):
    resp = {}

    pk = int(request.POST.get('id', None))
    newpassword = request.POST.get('newpassword', None)

    user = get_object_or_404(ApiUser, pk=pk)


    newpasswordHash = sha256.hash(newpassword)
    user.password = newpasswordHash

    user.save()  

    current_site = get_current_site(request) #"localhost:8000" #get_current_site(request)  
    mail_subject = 'Nueva contraseña para su cuenta en AlertaDo'  




    message = render_to_string('sini/api_user/new_password_email.html', {  
        'user': user,  
        'domain': current_site.domain,  
        'email': user.email,
        'newpassword':newpassword
    })  
    
    email_message = EmailMessage(  
                mail_subject, message, to=[user.email], from_email= settings.DEFAULT_FROM_EMAIL # "idec@deneb.io"  
    )  
    email_message.content_subtype = "html"  
    try:
        email_message.send()
    except Exception as e:
        resp['error'] = "Error al enviar el email"
        resp['error_description'] = str(e)
        return JsonResponse(resp, status=500)
    
    return JsonResponse(resp, status=200)


@login_required(login_url='/login/')
def api_user_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id = query['id']
    print(id)
   
    user = ApiUser.objects.get(id=id)
    #raise RestrictedError("Debe eliminar primero el bla bla ", warning)
    try:
        user.delete()
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