from howmuch.prestige.models import PrestigeLikeBuyer, PrestigeLikeSeller
from howmuch.core.models import Assignment
from howmuch.prestige.forms import PayConfirmForm, DeliveryConfirmForm, PrestigeLikeBuyerForm, PrestigeLikeSellerForm
from howmuch.prestige.functions import update_prestige
from howmuch.messages.models import Conversation, Message
from howmuch.notifications.models import Notification
from howmuch.notifications.functions import SendNotification
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import send_mail
from howmuch.core.functions import AssignmentFeatures

STATUS_ASSIGNMENT = (

	('0', 'NOTIFICADO'), #Cuando la Asignacion es generada
	('1', 'PAGADO'), #Cuando el comprador notifica el pago
	('2', 'PRODUCTO ENVIADO'), #Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
	('3','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
	('4', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
	('5', 'CANCELADO') #Cuando se cancela la transaccion

)

@login_required(login_url="/login/")
def confirmPay(request, assignmentID):

	"""
	Se Verifica que quien confirme el pago sea el COMPRADOR
	"""
	assignment = get_object_or_404(Assignment, pk = assignmentID, requestItem__owner = request.user)

	"""
	Se valida que la conversacion correspondiente a la asignacion exista, ya que enseguida se utiliza la variable
	"""

	conversation = get_object_or_404(Conversation, assignment = assignment)

	# Instancia de la clase AssignmentFeatures
	assignmentFeature = AssignmentFeatures(assignment)

	#Se valida que el pago no haya sido confirmado anteriormente
	if assignmentFeature.has_been_paid():
		return HttpResponse("Ya has confirmado este pago, no puedes confirmarlo nuevamente")
	elif request.method == 'POST':
		form = PayConfirmForm(request.POST, request.FILES)
		if form.is_valid():
			newPay = form.save(commit = False)
			newPay.owner = request.user
			newPay.assignment = assignment
			newPay.save()
			"""
			Se cambia el estado de la asignacion a 1
			"""
			assignment.status = "1"
			assignment.save()
			"""
			Se agrega a la conversacion de la asignacion el mensaje enviado en ConfirmPay
			"""
			#newMessage = Message.objects.create(owner = request.user, message = newPay.message, conversation = conversation)
			#newMessage.save()

			"""
			Se activa el sistema de Notificaciones
			"""

			newNotification = SendNotification(newPay,'confirm_pay')
			newNotification.sendNotification()


			return HttpResponseRedirect('/messages/' + str(conversation.pk) )
	else:
		form = PayConfirmForm()
	return render_to_response('prestige/payConfirm.html', { 'form' : form }, context_instance = RequestContext(request))
																			 
@login_required(login_url="/login/")
def confirmDelivery(request, assignmentID):
	"""
	Se verifica que quien confirma el envio sea el Vendedor
	"""
	assignment = get_object_or_404(Assignment, pk = assignmentID, owner = request.user)

	"""
	Se valida que la conversacion correspondiente a la asignacion exista, ya que enseguida se utiliza la variable
	"""

	conversation = get_object_or_404(Conversation, assignment = assignment)

	# Instancia de la clase AssignmentFeatures
	assignmentFeature = AssignmentFeatures(assignment)

	# Verifica que el pago haya sido realizado en caso de que no, envia mensaje de error
	if not assignmentFeature.has_been_paid():
		return HttpResponse("No puedes Confirmar el Envio del articulo hasta que el comprador no te haya pagado")

	#Se valida que la confirmacion del envio no haya sido confirmado anteriormente
	if assignmentFeature.has_been_delivered():
		return HttpResponse("Ya has confirmado el envio de este articulo, no puedes confirmarlo nuevamente")
	elif request.method == 'POST':
		form = DeliveryConfirmForm(request.POST, request.FILES)
		if form.is_valid():
			newDelivery = form.save(commit = False )
			newDelivery.owner = request.user
			newDelivery.assignment = assignment
			newDelivery.save()
			"""
			Se cambia el estado de la asignacion a 2
			"""
			assignment.status = "2"
			assignment.save()
			"""
			Se agrega a la conversacion de la asignacion el mensaje enviado en ConfirmPay
			"""
			#newMessage = Message.objects.create(owner = request.user, message = newDelivery.message, conversation = conversation)
			#newMessage.save()

			"""
			Se activa el sistema de notificaciones
			"""

			newNotification = SendNotification(newDelivery, 'confirm_delivery')
			newNotification.sendNotification()


			return HttpResponseRedirect('/messages/' + str(conversation.pk) )
			
	else:
		form = DeliveryConfirmForm()
	return render_to_response('prestige/deliveryConfirm.html', { 'form' : form }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def setPrestigeToSeller(request, assignmentID):
	assignment = get_object_or_404(Assignment, pk= assignmentID)

	#Valida que seas el Comprador del articulo para que puedas CRITICAR al vendedor

	if assignment.is_buyer(request.user):
		pass
	else:
		return HttpResponse("No tienes permiso para prestigiar a este usuario")

	#Se valida que esta critica no haya sido efectuado anteriormente

	try:
		PrestigeLikeSeller.objects.get(assignment = assignment, de = request.user)
	except PrestigeLikeSeller.DoesNotExist:
		pass
	else:
		return HttpResponse("Ya has criticado al Vendedor de este articulo, no puedes hacerlo nuevamente")

	if request.method == 'POST':
		form = PrestigeLikeSellerForm(request.POST)
		if form.is_valid():
			newPrestigeToSeller = form.save(commit = False)
			newPrestigeToSeller.de = request.user
			newPrestigeToSeller.to = assignment.owner
			newPrestigeToSeller.assignment = assignment
			newPrestigeToSeller.save()
			"""
			Se verifica si la asignacion ya posee critica de la contraparte, en caso que si se pasa a 4, si no a 3
			"""
			if assignment.has_been_critiqued_before():
				assignment.status = "4"
				assignment.save()
				update_prestige(request.user)
				update_prestige(assignment.owner)
			elif assignment.status == "2":
				assignment.status = "3"
				assignment.save()

			"""
			Se activa el sistema de Notificaciones
			"""

			newNotification = SendNotification(newPrestigeToSeller, 'critique')
			newNotification.sendNotification()
				
			return HttpResponseRedirect('/messages/' + str(assignment.conversation.pk) )
	else:
		form = PrestigeLikeSellerForm()
	return render_to_response('prestige/setPrestige.html' , { 'form' : form }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def setPrestigeToBuyer(request, assignmentID):
	assignment = get_object_or_404(Assignment, pk= assignmentID)

	#Valida que seas el Vendedor del articulo para que puedas CRITICAR al Comprador

	if assignment.is_seller(request.user):
		pass
	else:
		return HttpResponse("No tienes permiso para prestigiar a este usuario")


	#Se valida que esta critica no haya sido efectuado anteriormente

	try:
		PrestigeLikeBuyer.objects.get(assignment = assignment, de = request.user)
	except PrestigeLikeBuyer.DoesNotExist:
		pass
	else:
		return HttpResponse("Ya has criticado al Comprador de este articulo, no puedes hacerlo nuevamente")


	if request.method == 'POST':
		form = PrestigeLikeBuyerForm(request.POST)
		if form.is_valid():
			newPrestigeToBuyer = form.save(commit = False)
			newPrestigeToBuyer.de = request.user
			newPrestigeToBuyer.to = assignment.requestItem.owner
			newPrestigeToBuyer.assignment = assignment
			newPrestigeToBuyer.save()
			"""
			Se verifica si la asignacion ya posee critica de la contraparte, en caso que si se pasa a 4, si no a 3
			"""
			if assignment.has_been_critiqued_before():
				assignment.status = "4"
				assignment.save()
				update_prestige(request.user)
				update_prestige(assignment.requestItem.owner)
			elif assignment.status == "2":
				assignment.status = "3"
				assignment.save()

			"""
			Se activa el sistema de notificaciones
			"""

			newNotification = SendNotification(newPrestigeToBuyer, 'critique')
			newNotification.sendNotification()
	
			return HttpResponseRedirect('/messages/' + str(assignment.conversation.pk) )
	else:
		form = PrestigeLikeBuyerForm()
	return render_to_response('prestige/setPrestige.html' , { 'form' : form }, context_instance = RequestContext(request))










