from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from howmuch.article.functions import AboutAssignment
from howmuch.article.models import Assignment
from howmuch.messages.models import Conversation, Message
from howmuch.notifications.functions import NotificationOptions
from howmuch.notifications.models import Notification
from howmuch.prestige.forms import ConfirmPayForm, ConfirmDeliveryForm, CritiqueForm
from howmuch.prestige.functions import update_prestige, add_points, check_critique
from howmuch.prestige.models import Critique
from howmuch.settings import POINTS_FOR_CRITIQUE

STATUS_ASSIGNMENT = (

    ('1', 'NOTIFICADO'), #Cuando la Asignacion es generada
    ('2', 'PAGADO'), #Cuando el comprador notifica el pago
    ('3', 'PRODUCTO ENVIADO'), #Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
    ('4','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
    ('5', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
    ('6', 'CANCELADO') #Cuando se cancela la transaccion

)

@login_required(login_url="/login/")
def confirm_pay(request, assignmentID):
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
            #Se cambia el estado de la asignacion a 2
            assignment.status = "2"
            assignment.save()
            #Se envia notificacion
            NotificationOptions(newPay,'confirm_pay').send()
            return HttpResponseRedirect('/messages/' + str(conversation.pk) )
    else:
        form = ConfirmPayForm()
    return render_to_response('prestige/payConfirm.html', { 'form' : form }, context_instance = RequestContext(request))
                                                                             
@login_required(login_url="/login/")
def confirm_delivery(request, assignmentID):
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
            #Se cambia el estado de la asignacion a 3
            assignment.status = "3"
            assignment.save()            
            #Se activa el sistema de notificaciones
            NotificationOptions(newDelivery, 'confirm_delivery').send()
            return HttpResponseRedirect('/messages/' + str(conversation.pk) )   
    else:
        form = ConfirmDeliveryForm()
    return render_to_response('prestige/deliveryConfirm.html', { 'form' : form }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def critique(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk= assignmentID)
    #Valida que seas el Comprador o el vendedor para que puedas criticar
    if assignment.is_buyer(request.user):
        to = assignment.get_seller()
    elif assignment.is_seller(request.user):
        to = assignment.get_buyer()
    else:
        return HttpResponse("No tienes permiso para prestigiar a este usuario")
    #Se valida que esta critica no haya sido efectuado anteriormente
    try:
        Critique.objects.get(assignment = assignment, de = request.user)
    except Critique.DoesNotExist:
        pass
    else:
        return HttpResponse("Ya has criticado a tu socio, no puedes hacerlo nuevamente")

    if request.method == 'POST':
        form = CritiqueForm(request.POST)
        if form.is_valid():
            critique = form.save(commit = False)
            critique.de = request.user
            critique.to = to
            critique.assignment = assignment
            critique.save()
            #Se agregan puntos a quien critica
            add_points(request.user, POINTS_FOR_CRITIQUE)
            #Si la critica es positiva, se agregan 5 puntos, si es negativa se quitan 15 a la contraparte
            check_critique(critique,to)
            #Se verifica si la asignacion ya posee critica de la contraparte, en caso que si se pasa a 5, si no a 4
            if assignment.has_been_critiqued_before():
                assignment.status = "5"
                assignment.save()
                #Se actualiza el prestigio de los involucrados en la transaccion
                update_prestige(request.user)
                update_prestige(assignment.owner)
            elif assignment.status == "3":
                assignment.status = "4"
                assignment.save()
            #Se activa el sistema de Notificaciones
            NotificationOptions(critique, 'critique').send()                
            return HttpResponseRedirect('/messages/' + str(assignment.conversation.pk) )
    else:
        form =CritiqueForm()
    return render_to_response('prestige/critique.html' , { 'form' : form }, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def critiques(request, username):
    user = get_object_or_404(User, username=username)
    prestigeLikeBuyer = Critique.objects.filter(to__username = username).order_by('date')[:10]
    prestigeLikeSeller = Critique.objects.filter(to__username = username).order_by('date')[:10]
    return render_to_response('prestige/critiques.html', 
        {'prestigeLikeBuyer' : prestigeLikeBuyer, 'prestigeLikeSeller' : prestigeLikeSeller,
        'user' : user },
        context_instance=RequestContext(request))











