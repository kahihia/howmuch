# -*- coding: utf-8 -*-
from datetime import timedelta, date
import datetime
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from howmuch import settings
from howmuch.core.forms import AssignmentForm, OfferForm
from howmuch.core.functions import AboutArticle, AboutAssignment
from howmuch.core.models import Article, Offer, Assignment
from howmuch.messages.functions import InitialConversationContext
from howmuch.messages.models import Conversation
from howmuch.notifications.functions import SendNotification
from howmuch.notifications.models import Notification
from howmuch.perfil.models import Perfil
from howmuch.pictures.models import Picture
from howmuch.searchengine.views import indexArticle

from endless_pagination.decorators import page_template



TEMPLATES_NEWITEM = {'title' : 'newitemnew/title.html',
            'price' : 'newitemnew/price.html',
            'quantity' : 'newitemnew/quantity.html',
            'description' : 'newitemnew/description.html',
            'clasification' : 'newitemnew/clasification.html',
            'delivery' : 'newitemnew/delivery.html',
            'pictures' : 'newitemnew/pictures.html',
    
}

#Antes NewItemWizard
class Post(SessionWizardView):
    #Almacena imagenes de forma temporal, es necesaria esta linea segun la guia de django
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'pictures_temp'))

    def get_template_names(self):

        return [TEMPLATES_NEWITEM[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        form = super(NewItemWizard, self).get_form(step, data, files)
        if step == 'delivery':
            form.fields['addressDelivery'].queryset = self.request.user.perfil.addresses.all()
        return form

    def done(self, form_list,**kwargs):
        #Se gurdan los primeros 6 formularios
        instance = Article()
        for form in form_list[0:6]:
            for field, value in form.cleaned_data.iteritems():
                setattr(instance, field, value)
        instance.owner = self.request.user
        instance.save()
        #Se agrega el title_url
        instance.title_url = instance.title.replace(u'\xf1','n').replace(' ','-')
        instance.save()
        #Se gurdan el 4 formulario correspondiente a las imagenes
        for field, value in form_list[6].cleaned_data.iteritems():
            if value is not None:
                instancePicture = Picture()
                setattr(instancePicture, 'picture', value)
                instancePicture.owner = self.request.user
                instancePicture.save()
                #Se agrega la imagen al Articulo
                instance.pictures.add(instancePicture)
                instance.save()
        #Se anexa a la base de datos del motor de busqueda
        indexArticle(instance)
        #Se añade un +1 al total_purchases del usario
        perfilUser = get_object_or_404(Perfil, user = self.request.user)
        perfilUser.total_purchases += 1
        perfilUser.save()
        return HttpResponseRedirect(str(instance.get_url()))



@login_required(login_url="/login/")
#Decorador requerido para la app de paginacion tipo twitter
@page_template('core/home_index_page.html')
def home(
        request, template='core/home_index.html', extra_context=None):
    context = {
        'items': Article.objects.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

#Para ver un articulo no es necesario hacer login
def view(request, itemID, title_url):
    item = get_object_or_404(Article, pk=itemID)
    return render_to_response('core/viewItem.html', {'item' : item }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def offer(request,itemId):
    #Validar que el Article exista, si no existe regresa error 404
    Article = get_object_or_404(Article, pk = itemId)    
    #Se crea una instancia de AboutArticle, funcion que realiza algunas verificaciones
    aboutArticle = AboutArticle(request.user, itemId) 
    #Se valida la instancia: User is not candidate, is not owner, is not assigned
    if aboutArticle.is_valid():
        pass
    else:
        return render_to_response('core/candidatura.html', {'errors' : aboutArticle.errors() }, context_instance=RequestContext(request))
    #Formulario
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            pictures = []
            cprice = form.cleaned_data['cprice']
            message = form.cleaned_data['message']

            #Verifica cada campo de tipo input file, si el usuario lo uso, entonces lo agrega al diccionario para enseguida guardarlos
            pictures.append(form.cleaned_data['picture1'])
            if form.cleaned_data['picture2'] is not None:
                pictures.append(form.cleaned_data['picture2'])
            if form.cleaned_data['picture3'] is not None:
                pictures.append(form.cleaned_data['picture3'])
            if form.cleaned_data['picture4'] is not None:
                pictures.append(form.cleaned_data['picture4'])
            if form.cleaned_data['picture5'] is not None:
                pictures.append(form.cleaned_data['picture5'])

            thisOffer = Offer(owner=request.user, article = Article, cprice = cprice, message = message)
            thisOffer.save()

            #Guarda el diccionario de imagenes en thisOffer.pictures
            for picture in pictures:
                thisPicture = Picture(owner = request.user, picture = picture)
                thisPicture.save()
                thisOffer.pictures.add(thisPicture)
                thisOffer.save()

            #Se envia una notificacion 
            newNotification = SendNotification(newProffer, 'proffer')
            newNotification.sendNotification()


            return HttpResponseRedirect('/sales/possible/')
    else:
        form = ProfferForm()
    return render_to_response('core/candidatura.html', {'form' : form, 'Article' : Article, 'user' : request.user }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def viewCandidates(request, itemId):
    """
    Si cuenta con los parametros get notif_type and idBack, se hacen verificaciones y se actualiza la notificacion a has_been_readed = True
    """
    if request.GET.__contains__('notif_type') and request.GET.__contains__('idBack'):
        if request.GET['notif_type'] == 'proffer' and request.GET['idBack'] is not '' :
            idBack = request.GET['idBack']
            try:
                #Me aseguro que el usuario sea el dueño de la notificacion, que la notificacion este en False y la paso a True
                notification = Notification.objects.get(owner=request.user, tipo = 'proffer', has_been_readed = False ,idBack = idBack)
            except Notification.DoesNotExist:
                pass
            else:
                notification.has_been_readed = True
                notification.save()
                """
                Se le quita una notificacion al total de notificaciones del usuario
                """
                perfilUser = Perfil.objects.get(user = request.user)
                perfilUser.unread_notifications -= 1
                perfilUser.save()


    candidates = Proffer.objects.filter(Article = itemId)
    item = get_object_or_404(Article, pk = itemId)
    return render_to_response('core/candidatesList.html', {'candidates' : candidates, 'item' : item }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def newAssignment(request, itemId, candidateID):

    #Validar que el item exista y que el owner de el sea el request.user
    try:
        item = Article.objects.get(pk= itemId, owner=request.user)
    except Article.DoesNotExist:
        return HttpResponse("No tienes permiso para Asignar este Solicutud")
    else:
        pass
    
    candidate = get_object_or_404(Proffer, owner = candidateID, Article = item)
    candidateUser = get_object_or_404(User, pk = candidateID)

    #Validar que no exista Asignacion

    try:
        Assignment.objects.get(Article = item )
    except Assignment.DoesNotExist:
        pass
    else:
        return HttpResponse("Esta Asignacion ya Existe")

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            newAssignment = form.save(commit=False)
            newAssignment.owner = candidateUser 
            newAssignment.Article = item
            newAssignment.save()

            """
            Se crea la Conversation correspondiente a la Asignacion
            """
            conversation = Conversation.objects.create(assignment = newAssignment)
            conversation.save()

            """
            Se crea una instancia de InitialConversationContext
            """
            newContext = InitialConversationContext(item.owner, newAssignment.owner, conversation)
            newContext.createMessageByBuyer()
            newContext.createMessageBySeller()

            """
            Se Activa el Sistema de Notificaciones
            """

            newNotification = SendNotification(newAssignment,'assignment')
            newNotification.sendNotification()

            """
            se añade un +1 al total_sales del usuario
            """

            perfilUser = get_object_or_404(Perfil, user = newAssignment.owner)
            perfilUser.total_sales += 1
            perfilUser.save()


            return HttpResponse('Asignacion Correcta')
    else:
        form = AssignmentForm()
    return render_to_response('core/newAssignment.html', {'form' : form, 'candidateUser' : candidateUser, 'item' : item }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def publishedPurchasesView(request):
    items = Article.objects.filter(owner = request.user)
    publishedPurchases = []
    for item in items:
        if not item.has_assignment():
            publishedPurchases.append(item)
    return render_to_response('core/publishedPurchases.html', {'publishedPurchases' : publishedPurchases }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def processPurchasesView(request):
    items = Article.objects.filter(owner = request.user)
    processPurchases = []
    for item in items:
        if item.has_assignment() and not item.has_been_completed():
            processPurchases.append(item)
    return render_to_response('core/processPurchases.html', {'processPurchases' : processPurchases }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def completedPurchasesView(request):
    items = Article.objects.filter(owner = request.user)
    completedPurchases = []
    for item in items:
        if item.has_been_completed():
            completedPurchases.append(item)
    return render_to_response('core/completedPurchases.html', {'completedPurchases' : completedPurchases}, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def possibleSalesView(request):
    items = Proffer.objects.filter(owner = request.user )
    possibleSales = []
    for item in items:
        if item.is_open():
            possibleSales.append(item)
    return render_to_response('core/possibleSales.html', {'possibleSales' : possibleSales }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def processSalesView(request):
    processSales = Assignment.objects.filter(owner = request.user, status__in = ["0","1","2","3"])
    return render_to_response('core/processSales.html', {'processSales' : processSales}, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def completedSalesView(request):
    completedSales = Assignment.objects.filter(owner = request.user, status = "4")
    return render_to_response('core/completedSales.html', {'completedSales' : completedSales }, context_instance = RequestContext(request))



