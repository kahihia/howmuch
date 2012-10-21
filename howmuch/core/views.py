from howmuch.core.forms import RequestItemForm, ProfferForm, AssignmentForm
from howmuch.core.models import RequestItem, Proffer, Assignment
from howmuch.messages.models import Conversation
from howmuch.core.functions import UserRequestItem, AssignmentFeatures
from howmuch.messages.functions import InitialConversationContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta, date
from django.template import RequestContext
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
import datetime



TEMPLATES = {'description': 'newitem/description.html',
             'clasification': 'newitem/clasification.html',
             'delivery': 'newitem/delivery.html',
      	}

class NewItemWizard(SessionWizardView):
	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	def done(self, form_list,**kwargs):
		instance = RequestItem()
		for form in form_list:
			for field, value in form.cleaned_data.iteritems():
				setattr(instance, field, value)
		instance.owner = self.request.user
		instance.save()
		return HttpResponseRedirect('/pictures/addpicture/requestitem/' + str(instance.pk))

@login_required(login_url="/login/")
def home(request):
	items = RequestItem.objects.all()
	return render_to_response('core/home.html',{'items' : items } ,context_instance=RequestContext(request))

@login_required(login_url="/login/")
def requestItem(request):
	if request.method == 'POST':
		form = RequestItemForm(request.POST)
		if form.is_valid():
			#human = True
			newItem = form.save(commit=False)
			newItem.owner = request.user
			newItem.save()
			return HttpResponseRedirect('/pictures/addpicture/requestitem/' + str(newItem.pk) )
	else:
		form = RequestItemForm(initial={'addressDelivery' : request.user.get_profile().getAddressDelivery()})
	return render_to_response('core/newitem.html', {'form' : form}, context_instance=RequestContext(request))

def viewItem(request, itemID):
	item = get_object_or_404(RequestItem, pk=itemID)
	return render_to_response('core/viewItem.html', {'item' : item }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def newProffer(request,itemId):
	"""
	Validar que el RequestItem exista, si no existe regresa error 404
	"""

	requestItem = get_object_or_404(RequestItem, pk = itemId)

	"""
	Se crea una instancia de UserRequestItem
	"""

	userRequestItem = UserRequestItem(request.user, itemId)

	"""
	Se valida la instancia: User is not candidate, is not owner, is not assigned
	"""

	if userRequestItem.is_valid():
		pass
	else:
		return render_to_response('core/candidatura.html', {'errors' : userRequestItem.errors() }, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = ProfferForm(request.POST)
		if form.is_valid():
			newProffer = form.save(commit=False)
			newProffer.owner = request.user
			newProffer.requestItem = requestItem
			newProffer.save()

			"""
			Se envia email al comprador de que hay un nuevo candidato dispuesto a venderle el articulo
			"""

			subject = 'Hay un nuevo Vendedor para el articulo %s' % (newProffer.requestItem.title)

			message = '%s quiere venderte el articulo a $ %s, y para que lo elijas te dice lo siguiente: %s' % (newProffer.owner, newProffer.cprice,newProffer.message)

			to = [newProffer.requestItem.owner.email]

			send_mail(subject,message,'',to)

			return HttpResponseRedirect('/pictures/addpicture/proffer/' + str(newProffer.pk) )
	else:
		form = ProfferForm()
	return render_to_response('core/candidatura.html', {'form' : form, 'requestItem' : requestItem, 'user' : request.user }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def viewCandidates(request, itemId):
	candidates = Proffer.objects.filter(requestItem = itemId)
	return render_to_response('core/candidatesList.html', {'candidates' : candidates }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def newAssignment(request, itemId, candidateID):

	#Validar que el item exista y que el owner de el sea el request.user
	try:
		item = RequestItem.objects.get(pk= itemId, owner=request.user)
	except RequestItem.DoesNotExist:
		return HttpResponse("No tienes permiso para Asignar este Solicutud")
	else:
		pass
	
	candidate = get_object_or_404(Proffer, owner = candidateID, requestItem = item)
	candidateUser = get_object_or_404(User, pk = candidateID)

	#Validar que no exista Asignacion

	try:
		Assignment.objects.get(requestItem = item )
	except Assignment.DoesNotExist:
		pass
	else:
		return HttpResponse("Esta Asignacion ya Existe")

	if request.method == 'POST':
		form = AssignmentForm(request.POST)
		if form.is_valid():
			newAssignment = form.save(commit=False)
			newAssignment.owner = candidateUser 
			newAssignment.requestItem = item
			newAssignment.save()

			"""
			Se notifica al Candidato que ha sido seleccionado para vender el articulo por email
			"""

			subject = 'Has sido seleccionado para vender el articulo %s' % (newAssignment.requestItem.title)
			message = 'Esta es una confirmacion de que eres el Vendedor del articulo %s, enseguida recibiras un correo con la informacion de envio del articulo, el mensaje que el comprador te ha dejado es: %s ,puedes conversar con el comprador en el INBOX de howmuch' % (newAssignment.requestItem.title, newAssignment.comment)
			to = [newAssignment.owner.email]
			send_mail(subject, message, '', to)

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
			newContext.createMessageBySaller()

			return HttpResponseRedirect("/Thanks/")
	else:
		form = AssignmentForm()
	return render_to_response('core/newAssignment.html', {'form' : form}, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def publishedPurchasesView(request):
	items = RequestItem.objects.filter(owner = request.user)
	publishedPurchases = []
	for item in items:
		if not item.has_assignment():
			publishedPurchases.append(item)
	return render_to_response('core/publishedPurchases.html', {'publishedPurchases' : publishedPurchases }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def processPurchasesView(request):
	items = RequestItem.objects.filter(owner = request.user)
	processPurchases = []
	for item in items:
		if item.has_assignment():
			processPurchases.append(item)
	return render_to_response('core/processPurchases.html', {'processPurchases' : processPurchases }, context_instance = RequestContext(request))


@login_required(login_url="/login/")
def completedPurchasesView(request):
	items = RequestItem.objects.filter(owner = request.user)
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



