from django.contrib.auth.models import User
from howmuch.core.models import Assignment, RequestItem
from howmuch.messages.models import Conversation, Message

class InitialConversationContext:
	def __init__(self,buyer,saller, conversation):
		self.buyer = buyer
		self.saller = saller
		self.conversation = conversation

	def createMessageByBuyer(self):
		theMessage = "Hola " + str(self.saller.first_name) + ", la Direccion a la que quiero que envies el producto es: " + str(self.buyer.get_profile().getAddressDelivery()) 
		newMessage = Message.objects.create(owner = self.buyer, message = theMessage ,conversation = self.conversation )
		newMessage.save()


	def createMessageBySaller(self):
		theMessage = "Gracias, mi Banco es: " + str(self.saller.get_profile().bank) + " y mi CTA es: " + str(self.saller.get_profile().account_bank) + " , En cuanto este confirmado el Deposito, yo te enviare el Producto"
		newMessage = Message.objects.create(owner = self.saller, message = theMessage, conversation = self.conversation)
		newMessage.save()

