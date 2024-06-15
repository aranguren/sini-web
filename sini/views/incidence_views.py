from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from ..models import Incidence, MobileWarning, Contact, IncidenceType
from ..forms import IncidenceForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
import json 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string  
import csv
import io
from django.http import HttpResponse
import shapefile
from zipfile import ZipFile

class IncidenceListView(LoginRequiredMixin, ListView):
    model = Incidence
    template_name = 'sini/incidence/incidence_list.html'
    context_object_name = 'incidences'
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(IncidenceListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['sini','incidence']
        context['active_menu'] ='sini'

    


        if 'name' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True

        
        self.request.session['page_from'] = ""
        self.request.session['referer'] = {}

        incidences_types = IncidenceType.objects.all()
        context['incidences_types'] = incidences_types

        # aqui ponemos los valores a los filtros
        context['value_name'] = self.request.GET.get('name', '')
        context['value_type'] = self.request.GET.get('type', '')
        context['value_status'] = self.request.GET.get('status', '')
        context['value_active'] = self.request.GET.get('active', '')

        if context['is_paginated']:
            list_pages = []

            if 'name' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(IncidenceListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(IncidenceListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(IncidenceListView.get_queryset(self)) / self.paginate_by) + 1

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
        query = {
            'name': self.request.GET.get('name', None),
            'type': self.request.GET.get('type', None),
            'status': self.request.GET.get('status', None),
            'active': self.request.GET.get('active', None),
            }

        query_result =  Incidence.objects.order_by('-created')

        if query['active'] and query['active'] != '':
            if query['active']=='si':
                query_result = query_result.filter(active=True)
            elif query['active']=='no':
                query_result = query_result.filter(active=False)
            elif query['active']=='si_no':
                pass


        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])
        if query['type'] and query['type'] != '':
            type_id = query['type']
            type = IncidenceType.objects.get(id=type_id)
            query_result = query_result.filter(type_incidence=type )
        if query['status'] and query['status'] != '':
            query_result = query_result.filter(status__exact=query['status'])


  
        return query_result
    

class IncidenceDetailView(LoginRequiredMixin, DetailView):
    model = Incidence
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'incidence'
    template_name = 'sini/incidence/incidence_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini','incidence']
        context['active_menu'] ='sini'

        contactos = Contact.objects.all()
        context['contactos'] = contactos
        return context


class IncidenceCreateView(LoginRequiredMixin, CreateView):
    model = Incidence
    context_object_name = 'incidence'
    template_name = 'sini/incidence/incidence_form.html'
    form_class = IncidenceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ['sini', 'incidence']
        context['active_menu'] = 'sini'

        return context

    def get_success_url(self):
        return reverse_lazy("sini:incidence_detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        warning = form.save(commit=False)
        warning.created_by = self.request.user  # use your own profile here
        warning.save()
        return super(IncidenceCreateView, self).form_valid(form)


class IncidenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Incidence
    context_object_name = 'incidence'
    template_name = 'sini/incidence/incidence_form.html'
    form_class = IncidenceForm
    
    def get_success_url(self):
        return reverse_lazy("sini:incidence_detail", kwargs={"pk": self.object.id}) 

    def form_valid(self, form):
        api_user = form.save(commit=False)
        api_user.modified_by = self.request.user 
        return super(IncidenceUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini', 'incidence']
        context['active_menu'] = 'sini'
        
        return context


class IncidenceManagmentView(LoginRequiredMixin, TemplateView):
    template_name = 'sini/incidence/incidence_managment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini', 'managment']
        context['active_menu'] = 'sini'
        incidences = Incidence.objects.filter(active=True, status='creado').order_by("-created")
        mobile_warnings = MobileWarning.objects.filter(active=True, status='creado').order_by("-created")
        context['incidences'] = incidences
        context['mobile_warnings'] = mobile_warnings
        contactos = Contact.objects.all()
        context['contactos'] = contactos
       
        
        return context

@login_required(login_url='/login/')
def incidence_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id = query['id']
    print(id)
   
    incidence = Incidence.objects.get(id=id)
    #raise RestrictedError("Debe eliminar primero el bla bla ", warning)
    try:
        incidence.delete()
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



class IncidenceFinalizeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        incidence = get_object_or_404(Incidence, pk=pk)
        incidence.status = 'finalizado'
        incidence.save()
        redirection = reverse_lazy("sini:incidence_detail", kwargs={"pk": pk}) 
        return redirect(redirection)

class IncidenceArchiveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        incidence = get_object_or_404(Incidence, pk=pk)
        incidence.active = False
        incidence.save()
        redirection = reverse_lazy("sini:incidence_detail", kwargs={"pk": pk}) 
        return redirect(redirection)

class IncidenceActivateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        incidence = get_object_or_404(Incidence, pk=pk)
        incidence.active = True
        incidence.save()
        redirection = reverse_lazy("sini:incidence_detail", kwargs={"pk": pk}) 
        return redirect(redirection)
    

@login_required(login_url='/login/')
def incidence_archive(request, pk):
    resp = {}
    
    incidence = get_object_or_404(Incidence, pk=pk)

    incidence.active = False
    incidence.save()

    return JsonResponse(resp, status=200)

@login_required(login_url='/login/')
def incidence_finalize(request, pk):
    resp = {}
    
    incidence = get_object_or_404(Incidence, pk=pk)

    incidence.status = 'finalizado'
    incidence.save()

    return JsonResponse(resp, status=200)

import time
@login_required(login_url='/login/')
def incidence_send_email(request):
    resp = {}

    pk = request.POST.get('id', None)
    destinatarios = request.POST.get('destinatarios', None)

    destinatarios_obj = json.loads(destinatarios)
    listado_destinatarios  =[int(id) for id in destinatarios_obj]

    asunto = request.POST.get('asunto', None)
    mensaje = request.POST.get('mensaje', None)
    #time.sleep(10)
   
    incidence = get_object_or_404(Incidence, pk=pk)
    contact_list = get_list_or_404(Contact, id__in=listado_destinatarios)
    email_address_list=[]
    for contacto in contact_list:
        email_address_list.append(contacto.email)

    latitud = incidence.geom.y
    longitud  = incidence.geom.x

    message = render_to_string('sini/incidence/incidence_send_email.html', {  
                'mensaje':mensaje,
                'latitud':latitud,
                'longitud':longitud,
                'incidence': incidence, 

            })  
            
    email_message = EmailMessage(  
                f"Sistema SINI - {asunto}", message, to=email_address_list, from_email= settings.DEFAULT_FROM_EMAIL # "idec@deneb.io"  
    )  
    imagen1 = incidence.image1
    if imagen1:
        email_message.attach_file(incidence.image1.path)
    imagen2 = incidence.image2
    if imagen2:
        email_message.attach_file(incidence.image2.path)
    imagen3 = incidence.image3
    if imagen3:
        email_message.attach_file(incidence.image3.path)
    attachment_csv = generate_csv(incidence)
    email_message.attach('incidencia.csv', attachment_csv.read())

    email_message.content_subtype = "html"
    

    try:
        email_message.send()
    except Exception as e:
        resp['error'] = "Error al enviar el email"
        resp['error_description'] = str(e)
        return JsonResponse(resp, status=500)
   

    return JsonResponse(resp, status=200)



class ExportCsvIncidenceView(LoginRequiredMixin, View):

    def post(self, request):

        query_result = Incidence.objects.order_by('-created')


        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="incidencias.csv"'},
            )
        writer = csv.writer(response)
        #writer.writerow([])
        writer.writerow(['ID','Nombre','Fecha creación', 'Fecha última modificación', 'Prioridad','Tipo incidente','Status', 'Activo','Latitud','Longitud','Descripción'])

        for item in query_result:
            created = item.created.strftime("%d/%m/%Y, %H:%M:%S") if item.created else ""
            modified = item.modified.strftime("%d/%m/%Y, %H:%M:%S") if item.created else ""
            x =  item.geom.x if item.geom else ""
            y =  item.geom.y if item.geom else ""
          
            writer.writerow([item.id, item.name, created, modified, item.priority, item.type_incidence.name, item.status, 
                             "SI" if item.active else "NO", y, x, item.description])
      
        return response
    

class ExportShapefileIncidenceView(LoginRequiredMixin, View):

    def post(self, request):

        incidences = Incidence.objects.order_by('-created')

        """
        response = HttpResponse(
            content_type="application/force-download",
            headers={"Content-Disposition": 'attachment; filename="incidencias.shp"'},
            )
        """
        try:
            from StringIO import StringIO
        except ImportError:
            from io import BytesIO as StringIO
        
        shp = StringIO()
        shx = StringIO()
        dbf = StringIO()
        #shapefiles/test/testfile
        #w = shapefile.Writer("./warnings.shp", shapeType=shapefile.POINT)
        
        w = shapefile.Writer(shp=shp, shx=shx, dbf=dbf, shapeType=shapefile.POINT)
        w.autoBalance = 1
        w.field('ID', 'C', size=255)
        w.field('CREATED', 'D')
        w.field('CREATED_TIME', 'C')
        w.field('MODIFIED', 'D')
        w.field('MODIFIED_TIME', 'C')
        w.field('ACTIVE', 'L')
        w.field('NAME', 'C', size=255)
        w.field('TYPE_INCIDENCE', 'C', size=255)
        w.field('DESCRIPTION', 'C')
        w.field('STATUS', 'C', size=255)
        w.field('PRIORIDAD', 'N')

    
        for incidence in incidences:
            created = incidence.created.strftime("%Y%m%d") if incidence.created else None
            created_time = incidence.created.strftime("%H:%M:%S") if incidence.created else None
            modified = incidence.modified.strftime("%Y%m%d") if incidence.modified else None
            modified_time = incidence.modified.strftime("%H:%M:%S") if incidence.modified else None    

            w.record(ID=incidence.id, 
                     CREATED=created, 
                     CREATED_TIME=created_time, 
                     MODIFIED=modified, 
                     MODIFIED_TIME=modified_time, 
                     ACTIVE=incidence.active, 
                     NAME=incidence.name, 
                     TYPE_INCIDENCE=incidence.type_incidence.name,
                     DESCRIPTION=incidence.description,
                    STATUS=incidence.status, 
                    PRIORIDAD=incidence.priority)
            w.point(incidence.geom.x, incidence.geom.y) 
        
    
        w.close()
        mem_zip = StringIO()
        with ZipFile(mem_zip, 'w') as myzip:
            myzip.writestr("incidencias.shp", shp.getvalue())
            myzip.writestr("incidencias.dbf", dbf.getvalue())
            myzip.writestr("incidencias.shx", shx.getvalue())
            

        full_zip_in_memory = mem_zip.getvalue()

        response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('incidencias.zip')
    
        return response



def generate_csv(incidence: Incidence):
    file_output = io.StringIO()
    csv_writer = csv.writer(file_output, delimiter=',',                 
        quoting=csv.QUOTE_ALL)
    csv_writer.writerow(['NOMBRE', 'TIPO INCIDENTE', 'PRIORIDAD', 'FECHA CREACIÓN', 'LATITUD', 'LONGITUD', 'ESTADO', 'DESCRIPCIÓN'])
    csv_items = [incidence.name, 
                 incidence.type_incidence.name, 
                 str(incidence.priority),
                 incidence.created.strftime("%d/%m/%Y, %H:%M:%S"),
                 str(incidence.geom.y), 
                 str(incidence.geom.x), 
                 incidence.status, 
                 incidence.description]
    
    #for item in csv_items:
    csv_writer.writerow(csv_items)
    file_output.seek(0)
    return file_output