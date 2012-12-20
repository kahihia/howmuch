from django.contrib.auth.models import User
from django.core.mail import send_mail
from howmuch.core.models import Assignment, RequestItem
from howmuch.messages.models import Conversation, Message

class InitialConversationContext(object):
    def __init__(self,buyer,seller, conversation):
        self.buyer = buyer
        self.seller = seller
        self.conversation = conversation

    def createMessageByBuyer(self):
        """
        Se crea el mensaje de inicio del comprador
        """
        theMessage = "Hola " + str(self.seller.first_name) + ", la Direccion a la que quiero que envies el producto es: " + str(self.conversation.assignment.requestItem.addressDelivery.get_address())
        
        """
        se envia un mail con el mensaje de inicio del comprador para el vendedor
        """

        subject = 'Direccion de envio del articulo %s' % (self.conversation.assignment.requestItem.title)
        message = theMessage
        de = ''
        to = [str(self.seller.email)] 

        send_mail(subject,message,de,to)


    def createMessageBySeller(self):
        theMessage = "Gracias, las cuentas bancarias a las que me puedes depositar son: " + self.seller.perfil.get_banks() + " , En cuanto este confirmado el Deposito, yo te enviare el Producto"

        """
        se envia un mail con el mensaje de inicio del vendedor para el comprador
        """
        
        subject = 'Informacion de pago para el articulo %s' % (self.conversation.assignment.requestItem.title)
        message = theMessage
        de = ''
        to = [str(self.buyer.email)] 

        send_mail(subject,message,de,to)




