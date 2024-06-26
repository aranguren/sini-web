from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from ..models import MobileWarning, Incidence, IncidenceType
from ..forms import WarningForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
import json 
from django.contrib.gis.db.models.functions import Distance
import csv
from django.http import HttpResponse
import shapefile
from zipfile import ZipFile
from datetime import datetime


class WarningListView(LoginRequiredMixin, ListView):
    model = MobileWarning
    template_name = 'sini/warning/warning_list.html'
    context_object_name = 'warnings'
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(WarningListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['sini','warning']
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

                if len(WarningListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(WarningListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(WarningListView.get_queryset(self)) / self.paginate_by) + 1

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

        query_result =  MobileWarning.objects.order_by('-created')

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
    

class WarningDetailView(LoginRequiredMixin, DetailView):
    model = MobileWarning
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'warning'
    template_name = 'sini/warning/warning_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini','warning']
        context['active_menu'] ='sini'
        incidences = Incidence.objects.filter(active=True)
        context['incidences'] = incidences
        
        return context
   

class WarningDiscardView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        warning = get_object_or_404(MobileWarning, pk=pk)
        warning.status = 'descartado'
        warning.save()
        redirection = reverse_lazy("sini:warning_detail", kwargs={"pk": pk}) 
        return redirect(redirection)

class WarningArchiveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        warning = get_object_or_404(MobileWarning, pk=pk)
        warning.active = False
        warning.save()
        redirection = reverse_lazy("sini:warning_detail", kwargs={"pk": pk}) 
        return redirect(redirection)

class WarningActivateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        warning = get_object_or_404(MobileWarning, pk=pk)
        warning.active = True
        warning.save()
        redirection = reverse_lazy("sini:warning_detail", kwargs={"pk": pk}) 
        return redirect(redirection)
    
class WarningCreateView(LoginRequiredMixin, CreateView):
    model = MobileWarning
    context_object_name = 'warning'
    template_name = 'sini/warning/warning_form.html'
    form_class = WarningForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ['sini', 'warning']
        context['active_menu'] = 'sini'

        return context

    def get_success_url(self):
        return reverse_lazy("sini:warning_detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        warning = form.save(commit=False)
        #User = get_user_model()

        warning.created_by = self.request.user  # use your own profile here
        warning.creation_origin="web"
        warning.active=True
        #farm.active = True
        warning.save()
        return super(WarningCreateView, self).form_valid(form)


class WarningUpdateView(LoginRequiredMixin, UpdateView):
    model = MobileWarning
    context_object_name = 'warning'
    template_name = 'sini/warning/warning_form.html'
    form_class = WarningForm
    
    def get_success_url(self):
        return reverse_lazy("sini:warning_detail", kwargs={"pk": self.object.id}) 

    def form_valid(self, form):
        mobilewarning = form.save(commit=False)
        mobilewarning.modified_by = self.request.user 
        return super(WarningUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['sini', 'warning']
        context['active_menu'] = 'sini'
        
        return context


@login_required(login_url='/login/')
def warning_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id = query['id']
    print(id)
   
    warning = MobileWarning.objects.get(id=id)
    #raise RestrictedError("Debe eliminar primero el bla bla ", warning)
    try:
        warning.delete()
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

@login_required(login_url='/login/')
def warning_assign(request, pk):
    resp = {}
    #id = request.GET.get('id', None)
    incidence_id = request.GET.get('incidence_id', None)
    
    warning = get_object_or_404(MobileWarning, pk=pk)
    incidence = get_object_or_404(Incidence, pk=incidence_id)
    warning.assign_incidence = incidence
    warning.status = 'asignado'
    warning.save()

    return JsonResponse(resp, status=200)

@login_required(login_url='/login/')
def warning_create_incidence(request, pk):
    resp = {}
    #id = request.GET.get('id', None)
    prioridad = int(request.GET.get('prioridad', None))
    
    warning = get_object_or_404(MobileWarning, pk=pk)
    new_incidence = Incidence(
        name=warning.name,
        geom=warning.geom,
        type_incidence=warning.type_incidence,
        description=warning.description,
        status='creado',
        priority=prioridad,
        image1=warning.image1,
        image2=warning.image2,
        image3=warning.image3,
        audio=warning.audio,
        video=warning.video,
        created_by=request.user

    )
    new_incidence.save()
    #incidence = get_object_or_404(Incidence, pk=incidence_id)
    #warning.assign_incidence = incidence
    #warning.status = 'asignado'
    warning.assign_incidence = new_incidence
    warning.status = 'asignado'
    warning.save()

    incidence_feature = {
      "type": "Feature",
        "id": new_incidence.id,
      "properties": {
          "name": new_incidence.name,
          "description": new_incidence.description,
          "type_incidence_str": new_incidence.type_incidence.name,
          "status": new_incidence.status,
          "priority": new_incidence.priority,
          "id": new_incidence.id,
          "date": new_incidence.created.strftime("%d/%m/%Y, %H:%M:%S")

      },
      "geometry": {
          "type": "Point",
          "coordinates": [new_incidence.geom.x, new_incidence.geom.y ]
      }
    };
    warning_feature = {
      "type": "Feature",
        "id": warning.id,
      "properties": {
          "name": warning.name,
          "description": warning.description,
          "type_incidence_str": warning.type_incidence.name,
          "status": warning.status,

      },
      "geometry": {
          "type": "Point",
          "coordinates": [warning.geom.x, warning.geom.y ]
      }
    };
    resp['incidenceFeature'] = incidence_feature
    resp['warningFeature'] = warning_feature


    return JsonResponse(resp, status=200)


@login_required(login_url='/login/')
def warning_assign_closest(request, pk):
    resp = {}
    #id = request.GET.get('id', None)
    
    
    warning = get_object_or_404(MobileWarning, pk=pk)
    active_incidences = Incidence.objects.filter(active=True).exclude(status__iexact='finalizado')
    incidence = active_incidences.annotate(
                    distance=Distance('geom', warning.geom)
                ).order_by('distance').first()
    if incidence:
        warning.assign_incidence = incidence
        warning.status = 'asignado'
        warning.save()

        incidence_feature = {
            "type": "Feature",
                "id": incidence.id,
            "properties": {
                "name": incidence.name,
                "description": incidence.description,
                "type_incidence_str": incidence.type_incidence.name,
                "status": incidence.status,
                "priority": incidence.priority

            },
            "geometry": {
                "type": "Point",
                "coordinates": [incidence.geom.x, incidence.geom.y ]
            }
            };
        warning_feature = {
        "type": "Feature",
            "id": warning.id,
        "properties": {
            "name": warning.name,
            "description": warning.description,
            "type_incidence_str": warning.type_incidence.name,
            "status": warning.status,

        },
        "geometry": {
            "type": "Point",
            "coordinates": [warning.geom.x, warning.geom.y ]
        }
        };
    
        resp['incidenceFeature'] = incidence_feature
        resp['warningFeature'] = warning_feature

    else:
        resp['mensaje'] = 'no_incidence'
        return JsonResponse(resp, status=400)

    

    return JsonResponse(resp, status=200)


@login_required(login_url='/login/')
def warning_archive(request, pk):
    resp = {}
    
    warning = get_object_or_404(MobileWarning, pk=pk)

    warning.active = False
    warning.save()

    return JsonResponse(resp, status=200)

@login_required(login_url='/login/')
def warning_toss(request, pk):
    resp = {}
    
    warning = get_object_or_404(MobileWarning, pk=pk)

    warning.status = 'descartado'
    warning.save()

    return JsonResponse(resp, status=200)


class ExportCsvWarningView(LoginRequiredMixin, View):

    def post(self, request):

        query_result = MobileWarning.objects.order_by('-created')


        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="avisos.csv"'},
            )
        writer = csv.writer(response)
        #writer.writerow([])
        writer.writerow(['ID','Nombre','Fecha creación','Fecha última modificación', 'Tipo incidente','Status','Incidencia', 'Activo','Latitud','Longitud','Descripción'])

        for item in query_result:
            created = item.created.strftime("%d/%m/%Y, %H:%M:%S") if item.created else ""
            modified = item.modified.strftime("%d/%m/%Y, %H:%M:%S") if item.created else ""
            x =  item.geom.x if item.geom else ""
            y =  item.geom.y if item.geom else ""
          
            writer.writerow([item.id, item.name, created, modified, item.type_incidence.name, item.status, item.assign_incidence.name if item.assign_incidence else "",
                             "SI" if item.active else "NO", y, x, item.description])
      
        return response


class ExportShapefileWarningView(LoginRequiredMixin, View):

    def post(self, request):

        mobile_warnings = MobileWarning.objects.order_by('-created')

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
        w.field('ASSIGN_INCIDENCE', 'C', size=255)

    
        for mwarning in mobile_warnings:
            created = mwarning.created.strftime("%Y%m%d") if mwarning.created else None
            created_time = mwarning.created.strftime("%H:%M:%S") if mwarning.created else None
            modified = mwarning.modified.strftime("%Y%m%d") if mwarning.modified else None
            modified_time = mwarning.modified.strftime("%H:%M:%S") if mwarning.modified else None    

            w.record(ID=mwarning.id, 
                     CREATED=created, 
                     CREATED_TIME=created_time, 
                     MODIFIED=modified, 
                     MODIFIED_TIME=modified_time, 
                     ACTIVE=mwarning.active, 
                     NAME=mwarning.name, 
                     TYPE_INCIDENCE=mwarning.type_incidence.name,
                     DESCRIPTION=mwarning.description,
                    STATUS=mwarning.status, 
                    ASSIGN_INCIDENCE=mwarning.assign_incidence.name if mwarning.assign_incidence else None)
            w.point(mwarning.geom.x, mwarning.geom.y) 
        
    
        w.close()
        mem_zip = StringIO()
        with ZipFile(mem_zip, 'w') as myzip:
            myzip.writestr("avisos.shp", shp.getvalue())
            myzip.writestr("avisos.dbf", dbf.getvalue())
            myzip.writestr("avisos.shx", shx.getvalue())
            

        full_zip_in_memory = mem_zip.getvalue()

        response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('avisos.zip')
    
        return response
    
"""
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
        return reverse_lazy("sini:api_user_detail_detail", kwargs={"pk":self.object.id})   

    def form_valid(self, form):
        api_user = form.save(commit=False)
        api_user.modified_by = self.request.user 
        return super(ApiUserUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['appmobile','api_user']
        context['active_menu'] ='appmobile'
        
        return context

"""