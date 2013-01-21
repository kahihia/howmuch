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
from howmuch.article.forms import AssignmentForm, OfferForm
from howmuch.article.functions import AboutArticle, AboutAssignment
from howmuch.article.models import Article, Offer, Assignment
from howmuch.messages.functions import ConversationOptions
from howmuch.messages.models import Conversation
from howmuch.notifications.functions import NotificationOptions
from howmuch.notifications.models import Notification
from howmuch.profile.models import Profile
from howmuch.pictures.models import Picture


TEMPLATES_NEWITEM = {'title' : 'article/title.html',
            'price' : 'article/price.html',
            'quantity' : 'article/quantity.html',
            'description' : 'article/description.html',
            'clasification' : 'article/clasification.html',
            'delivery' : 'article/delivery.html',
            'pictures' : 'article/pictures.html',
    
}

class Post(SessionWizardView):
    #Almacena imagenes de forma temporal, es necesaria esta linea segun la guia de django
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'pictures_temp'))

    def get_template_names(self):

        return [TEMPLATES_NEWITEM[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        form = super(Post, self).get_form(step, data, files)
        if step == 'delivery':
            form.fields['addressDelivery'].queryset = self.request.user.profile.addresses.all()
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

        #Se anade un +1 al total_purchases del usario
        profileUser = get_object_or_404(Profile, user = self.request.user)
        profileUser.total_purchases += 1
        profileUser.save()
        return HttpResponseRedirect(str(instance.get_url()))


#Para ver un articulo no es necesario hacer login
def view(request, itemID, title_url):
    item = get_object_or_404(Article, pk=itemID)
    return render_to_response('article/viewItem.html', {'item' : item }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def offer(request,itemId):
    #Validar que el Article exista, si no existe regresa error 404
    article = get_object_or_404(Article, pk = itemId)    
    #Se crea una instancia de AboutArticle, funcion que realiza algunas verificaciones
    aboutArticle = AboutArticle(request.user, itemId) 
    #Se valida la instancia: User is not candidate, is not owner, is not assigned
    if aboutArticle.is_valid():
        pass
    else:
        return render_to_response('article/candidatura.html', {'errors' : aboutArticle.errors() }, context_instance=RequestContext(request))
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

            thisOffer = Offer(owner=request.user, article = article, cprice = cprice, message = message)
            thisOffer.save()

            #Guarda el diccionario de imagenes en thisOffer.pictures
            for picture in pictures:
                thisPicture = Picture(owner = request.user, picture = picture)
                thisPicture.save()
                thisOffer.pictures.add(thisPicture)
                thisOffer.save()

            #Se envia una notificacion 
            newNotification = NotificationOptions(thisOffer, 'offer')
            newNotification.send()


            return HttpResponseRedirect('/account/sales/possible/')
    else:
        form = OfferForm()
    return render_to_response('article/candidatura.html', {'form' : form, 'article' : article, 'user' : request.user }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def candidates(request, itemId):
    """
    Si cuenta con los parametros get notif_type and idBack, se hacen verificaciones y se actualiza la notificacion a has_been_readed = True
    """
    if request.GET.__contains__('notif_type') and request.GET.__contains__('idBack'):
        if request.GET['notif_type'] == 'offer' and request.GET['idBack'] is not '' :
            idBack = request.GET['idBack']
            try:
                #Me aseguro que el usuario sea el dueno de la notificacion, que la notificacion este en False y la paso a True
                notification = Notification.objects.get(owner=request.user, tipo = 'offer', has_been_readed = False ,idBack = idBack)
            except Notification.DoesNotExist:
                pass
            else:
                notification.has_been_readed = True
                notification.save()
                """
                Se le quita una notificacion al total de notificaciones del usuario
                """
                profileUser = Profile.objects.get(user = request.user)
                profileUser.unread_notifications -= 1
                profileUser.save()


    candidates = Offer.objects.filter(article = itemId)
    article = get_object_or_404(Article, pk = itemId)
    return render_to_response('article/candidatesList.html', {'candidates' : candidates, 'article' : article }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def assignment(request, itemId, candidateID):

    #Validar que el item exista y que el owner de el sea el request.user
    try:
        item = Article.objects.get(pk= itemId, owner=request.user)
    except Article.DoesNotExist:
        return HttpResponse("No tienes permiso para Asignar este Solicutud")
    else:
        pass
    
    candidate = get_object_or_404(Offer, owner = candidateID, article = item)
    candidateUser = get_object_or_404(User, pk = candidateID)

    #Validar que no exista Asignacion

    try:
        Assignment.objects.get(article = item )
    except Assignment.DoesNotExist:
        pass
    else:
        return HttpResponse("Esta Asignacion ya Existe")

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            newAssignment = form.save(commit=False)
            newAssignment.owner = candidateUser 
            newAssignment.article = item
            newAssignment.save()
            #Se crea la Conversation correspondiente a la Asignacion
            conversation = Conversation.objects.create(assignment = newAssignment)
            conversation.save()
            #Se crea una instancia de InitialConversationContext
            newContext = ConversationOptions(item.owner, newAssignment.owner, conversation)
            newContext.createMessageByBuyer()
            newContext.createMessageBySeller()
            #Se Activa el Sistema de Notificaciones
            newNotification = NotificationOptions(newAssignment,'assignment')
            newNotification.send()
            #se anade un +1 al total_sales del usuario
            profileUser = get_object_or_404(Profile, user = newAssignment.owner)
            profileUser.total_sales += 1
            profileUser.save()

            return HttpResponse('Asignacion Correcta')
    else:
        form = AssignmentForm()
    return render_to_response('article/newAssignment.html', {'form' : form, 'candidateUser' : candidateUser, 'item' : item }, context_instance=RequestContext(request))


