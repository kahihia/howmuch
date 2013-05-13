from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.utils import simplejson

from howmuch.article.forms import ArticleForm, AssignmentForm, OfferForm
from howmuch.article.functions import AboutArticle, AboutAssignment, validate_assignment, validate_offer, save_post_pictures
from howmuch.article.models import Article, Offer, Assignment
from howmuch.invoice.functions import generate_charge, check_invoice
from howmuch.messages.models import Conversation
from howmuch.messages.views import update_status_notification
from howmuch.notifications.functions import NotificationOptions
from howmuch.notifications.models import Notification
from howmuch.pictures.models import Picture
from howmuch.pictures.downloads import download_picture
from howmuch.prestige.functions import add_points
from howmuch.profile.models import Profile
from howmuch.search.views import index_article
from howmuch.settings import POINTS_FOR_PUBLISH, POINTS_FOR_OFFER, POINTS_FOR_SELECT, POINTS_FOR_ASSIGNMNET
from howmuch.category.functions import categories_matches


@login_required(login_url='/login/')
def post(request):
    from howmuch.tags.functions import input_to_words, add_tags
    #Si la cuenta de usuario esta bloqueada que lo indique
    if request.user.profile.is_block == True:
        return HttpResponse('Tu Cuenta esta bloqueada')
    #Formulario
    if request.method == 'POST':
        form=ArticleForm(request.POST)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.owner = request.user
            #Se genera el campo url sustituyendo caracteres
            newPost.title_url=newPost.title.replace(u'\xf1', 'n').replace(' ','-')
            newPost.save()
            #Se agregan los tags
            words = input_to_words(request.POST['tags'])
            add_tags(words,request.POST['category'], newPost)
            #Download pictures
            pictures = download_picture(newPost.title)
            save_post_pictures(newPost,pictures)
            #Se anade un +1 al total_purchases del usario
            request.user.profile.add_purchases()
            #Se indexa al motor de busqueda searchify
            index_article(newPost)
            #Se agregan 5 puntos Positivos a quien publica la compra, Action 1
            add_points(request.user, POINTS_FOR_PUBLISH)
            return HttpResponseRedirect(str(newPost.get_url()) + '?new_post=True')
    else:
        form=ArticleForm()
    return render_to_response('article/post.html', {'form' : form }, context_instance = RequestContext(request))

def edit(request, articleID, title_url):
    current = get_object_or_404(Article, pk = articleID, owner = request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance = current)
        if form.is_valid():
            post_edited = form.save()
            return HttpResponseRedirect(str(post_edited.get_url()))
    else:
        form = ArticleForm(instance=current)
    return render_to_response('article/post.html', {'form' : form }, context_instance = RequestContext(request))

#Para ver un articulo no es necesario hacer login
def view(request, articleID, title_url):
    article = get_object_or_404(Article, pk=articleID)
    if request.GET.__contains__('new_post') and request.GET['new_post']:
        new_post = True
    else:
        new_post = False
    return render_to_response('article/viewArticle.html', {'article' : article, 'new_post' : new_post }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def delete_picture(request, articleID, pictureID):
    a1 = get_object_or_404(Article, pk=articleID)
    p1 = get_object_or_404(Picture, pk=pictureID)
    a1.pictures.remove(p1)
    return render_to_response('article/viewArticle.html', {'article' : a1, 'new_post' : False }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def offer(request,articleID):
    #Si la cuenta de usuario esta bloqueada que lo indique
    if request.user.profile.is_block:
        return HttpResponse('Tu Cuenta esta bloqueada')
    #Validar que el Article exista, si no existe regresa error 404
    article = get_object_or_404(Article, pk = articleID)    
    #Validar Offer
    errors = validate_offer(articleID, request.user)
    #Formulario
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            pictures=[]
            quantity=form.cleaned_data['quantity'] 
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

            thisOffer = Offer.objects.create(owner=request.user, article=article, quantity=quantity ,cprice=cprice, message=message)
            thisOffer.save()

            #Guarda el diccionario de imagenes en thisOffer.pictures
            for picture in pictures:
                thisPicture = Picture(owner = request.user, picture = picture)
                thisPicture.save()
                thisOffer.pictures.add(thisPicture)
                thisOffer.save()

            #Se envia una notificacion 
            NotificationOptions(thisOffer, 'offer').send()

            #Se agregan 5 puntos Positivos a quien realiza la oferta, Action 2
            add_points(request.user, POINTS_FOR_OFFER)

            return HttpResponseRedirect('/account/offers/')
    else:
        form = OfferForm()
    return render_to_response('article/offer.html', {'form' : form, 'article' : article, 
            'user' : request.user, 'errors':errors }, 
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def offer_view(request, offerID):
    offer = get_object_or_404(Offer, pk=offerID, article__owner=request.user )
    return render_to_response('article/view_offer.html', {'offer' : offer}, 
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def my_offer(request,offerID):
    offer = get_object_or_404(Offer, pk=offerID, owner=request.user)
    return render_to_response('article/my_offer.html',{'offer':offer}, 
        context_instance=RequestContext(request))

@login_required(login_url="/login/")
def candidates(request, articleID):
    #Actualiza las notificaciones sin leer
    update_status_notification(request)
    candidates = Offer.objects.filter(article = articleID)
    article = get_object_or_404(Article, pk = articleID)
    return render_to_response('article/candidatesList.html', {'candidates' : candidates, 'article' : article }, 
        context_instance=RequestContext(request))

@login_required(login_url="/login/")
def assignment(request, articleID, candidateID):
    validate_assignment(articleID, request)
    article = get_object_or_404(Article, pk = articleID)
    offer = get_object_or_404(Offer, owner = candidateID, article = article)
    candidate = get_object_or_404(User, pk = candidateID)
    invoice = candidate.profile.get_current_invoice()
    #Formulario
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            newAssignment = form.save(commit=False)
            newAssignment.owner = candidate
            newAssignment.article = article
            newAssignment.save()
            #Articulo pasa a NO Activo
            article.is_active = False
            article.save()
            #Se genera un cargo a la factura del vendedor seleccionado
            generate_charge(newAssignment,offer.cprice, invoice)
            #Se checa la factura actual, si excede el limite, se asigna fecha limite de pago
            check_invoice(invoice)
            #Agregar puntos tanto al comprador por seleccionar, asi como al vendedor
            add_points(request.user, POINTS_FOR_SELECT)
            add_points(candidate, POINTS_FOR_ASSIGNMNET)
            #Enviar Notificacion
            NotificationOptions(newAssignment, 'assignment').send()
            
            return HttpResponseRedirect('/messages/' + str(newAssignment.conversation.pk))
    else:
        form = AssignmentForm()
    return render_to_response('article/assignment.html', {'form' : form, 'candidate' : candidate, 'article' : article }, 
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def get_article_tags(request):
    tags = Article.tags.all()
    json_response = simplejson.dumps( [{'val': tag.name} for tag in tags] )
    return HttpResponse(json_response)
