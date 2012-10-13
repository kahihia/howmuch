from howmuch.core.models import RequestItem, Proffer, Assignment
from howmuch.prestige.models import PayConfirm, DeliveryConfirm, Prestige
from howmuch.messages.models import Conversation



class UserRequestItem:
	def __init__(self, user, itemid):
		self.user = user
		self.requestItemId = itemid

	"""

	Regresa True si el Usuario es Propietario del RequestItem dado su id


	"""

	def is_owner(self):
		try:
			RequestItem.objects.get(owner = self.user, pk=self.requestItemId)
		except RequestItem.DoesNotExist:
			return False
		return True 

	"""

	Regresa True si el Usuario es Candidato del RequestItem dado su id, Es cuando el usuario da click en VENDER

	"""

	def is_candidate(self):
		try:
			Proffer.objects.get(owner = self.user, requestItem = self.requestItemId)
		except Proffer.DoesNotExist:
			return False
		return True

	"""
	
	Regresa True si el Usuario ha sido Asignado para completar el RequestItem (De los que dieron click en VENDER, es el que fue elegido)

	"""

	def is_assigned(self):
		try:
			Assignment.objects.get(requestItem = self.requestItemId)
		except Assignment.DoesNotExist:
			return False
		return True

	"""

	Regresa los Errores encontrados a la hora de realizar de intentar VENDER el articulo

	"""

	def errors(self):
		errors = []
		if self.is_owner():
			errors.append("Esta Solicitud fue publicada por ti y tu no puedes vendertela a ti mismo")
		elif self.is_assigned():
			errors.append("Este Articulo ya tiene Asignado un Vendedor, lo sentimos mucho")
		elif self.is_candidate():
			errors.append("Tu ya eres un Vendedor Candidaro, no puedes volver a serlo para este mismo articulo")
		
		return errors

	"""
	
	Regresa False en caso de que Sea Propietario, Candidato o Asignado dado el id del RequestItem

	"""

	def is_valid(self):
		if self.is_owner() or self.is_candidate() or self.is_assigned():
			return False
		return True

class AssignmentFeatures:
	def __init__(self, assignment):
		self.assignment = assignment

	def has_been_paid(self):
		try:
			PayConfirm.objects.get(assignment = self.assignment)
		except PayConfirm.DoesNotExist:
			return False
		return True

	def has_been_delivered(self):
		try:
			DeliveryConfirm.objects.get(assignment = self.assignment)
		except DeliveryConfirm.DoesNotExist:
			return False
		return True

	def has_been_critiqued(self):
		prestige = Prestige.objects.filter(assignment = self.assignment)
		if prestige.exists():
			return True
		return False

	def has_been_completed(self):
		if Prestige.objects.filter(assignment = self.assignment).count() == 2:
			return True
		return False

	def user_has_critiqued(self, user):
		try:
			Prestige.objects.filter(assignment = self.assignment, de = user)
		except Prestige.DoesNotExist:
			return False
		return True

	def is_in_process(self):
		if self.assignment.status in ["0", "1", "2", "3"]:
			return True
		return False






