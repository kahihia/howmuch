from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from howmuch.article.functions import AboutAssignment
from howmuch.article.models import Assignment
from howmuch.invoice.functions import generate_commission
from howmuch.messages.models import Conversation, Message
from howmuch.notifications.functions import NotificationOptions
from howmuch.notifications.models import Notification
from howmuch.prestige.forms import ConfirmPayForm, ConfirmDeliveryForm, PrestigeLikeBuyerForm, PrestigeLikeSellerForm
from howmuch.prestige.functions import update_prestige
from howmuch.prestige.models import PrestigeLikeBuyer, PrestigeLikeSeller

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
    #Se Verifica que quien confirme el pago sea el COMPRADOR
    assignment = get_object_or_404(Assignment, pk = assignmentID, article__owner = request.user)
    #Se valida que la conversacion correspondiente a la asignacion exista, ya que enseguida se utiliza la variable
    conversation = get_object_or_404(Conversation, assignment = assignment)
    # Instancia de la clase AboutAssignment
    aboutAssignment = AboutAssignment(assignment)
    #Se valida que el pago no haya sido confirmado anteriormente
    if aboutAssignment.has_been_paid():
        return HttpResponse("Ya has confirmado este pago, no puedes confirmarlo nuevamente")
    #Formulario
    elif request.method == 'POST':
        form = ConfirmPayForm(request.POST, request.FILES)
        if form.is_valid():
            newPay = form.save(commit = False)
            newPay.owner = request.user
            newPay.assignment = assignment
            newPay.save()
            #Se cambia el estado de la asignacion a 1
            assignment.status = "1"
            assignment.save()
            #Se envia notificacion
            NotificationOptions(newPay,'confirm_pay').send()
            return HttpResponseRedirect('/messages/' + str(conversation.pk) )
    else:
        form = ConfirmPayForm()
    return render_to_response('prestige/payConfirm.html', { 'form' : form }, context_instance = RequestContext(request))
                                                                             
@login_required(login_url="/login/")
def confirmDelivery(request, assignmentID):
    #Se verifica que quien confirma el envio sea el Vendedor
    assignment = get_object_or_404(Assignment, pk = assignmentID, owner = request.user)
    #Se valida que la conversacion correspondiente a la asignacion exista, ya que enseguida se utiliza la variable
    conversation = get_object_or_404(Conversation, assignment = assignment)
    # Instancia de la clase AboutAssignment
    aboutAssignment = AboutAssignment(assignment)    
    #Se valida que la confirmacion del envio no haya sido confirmado anteriormente
    if aboutAssignment.has_been_delivered():
        return HttpResponse("Ya has confirmado el envio de este articulo, no puedes confirmarlo nuevamente")
    #Formulario
    elif request.method == 'POST':
        form = ConfirmDeliveryForm(request.POST, request.FILES)
        if form.is_valid():
            newDelivery = form.save(commit = False )
            newDelivery.owner = request.user
            newDelivery.assignment = assignment
            newDelivery.save() 
            #Se cambia el estado de la asignacion a 2
            assignment.status = "2"
            assignment.save()            
            #Se activa el sistema de notificaciones
            NotificationOptions(newDelivery, 'confirm_delivery').send()
            return HttpResponseRedirect('/messages/' + str(conversation.pk) )   
    else:
        form = ConfirmDeliveryForm()
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
            #Se verifica si la asignacion ya posee critica de la contraparte, en caso que si se pasa a 4, si no a 3
            if assignment.has_been_critiqued_before():
                assignment.status = "4"
                assignment.save()
                update_prestige(request.user)
                update_prestige(assignment.owner)
            elif assignment.status == "2":
                assignment.status = "3"
                assignment.save()
                #Se genera el cargo por comision al vendedor
                generate_commission(assignment)
            #Se activa el sistema de Notificaciones
            NotificationOptions(newPrestigeToSeller, 'critique').send()                
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
    #Formulario
    if request.method == 'POST':
        form = PrestigeLikeBuyerForm(request.POST)
        if form.is_valid():
            newPrestigeToBuyer = form.save(commit = False)
            newPrestigeToBuyer.de = request.user
            newPrestigeToBuyer.to = assignment.article.owner
            newPrestigeToBuyer.assignment = assignment
            newPrestigeToBuyer.save()
            #Se verifica si la asignacion ya posee critica de la contraparte, en caso que si se pasa a 4, si no a 3
            if assignment.has_been_critiqued_before():
                assignment.status = "4"
                assignment.save()
                update_prestige(request.user)
                update_prestige(assignment.article.owner)
            elif assignment.status == "2":
                assignment.status = "3"
                assignment.save()
                #Se genera el cargo por comision al vendedor
                generate_commission(assignment)
            #Se activa el sistema de notificaciones
            NotificationOptions(newPrestigeToBuyer, 'critique').send()
            return HttpResponseRedirect('/messages/' + str(assignment.conversation.pk) )
    else:
        form = PrestigeLikeBuyerForm()
    return render_to_response('prestige/setPrestige.html' , { 'form' : form }, context_instance = RequestContext(request))

@login_required(login_url='/login/')
def critiques(request, username):
    user = get_object_or_404(User, username=username)
    prestigeLikeBuyer = PrestigeLikeBuyer.objects.filter(to__username = username).order_by('date')[:10]
    prestigeLikeSeller = PrestigeLikeSeller.objects.filter(to__username = username).order_by('date')[:10]
    return render_to_response('prestige/critiques.html', 
        {'prestigeLikeBuyer' : prestigeLikeBuyer, 'prestigeLikeSeller' : prestigeLikeSeller,
        'user' : user },
        context_instance=RequestContext(request))












