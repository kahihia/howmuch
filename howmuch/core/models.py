from django.db import models
from django.contrib.auth.models import User
from howmuch.pictures.models import Picture
from howmuch.items.models import ItemsCatA, ItemsCatB, ItemsCatC
from smart_selects.db_fields import ChainedForeignKey



STATES_CHOICES = (

	('NUEVO' , 'NUEVO'),
	('USADO' , 'USADO'),

)

STATUS_ASSIGNMENT = (

	('0', 'NOTIFICADO'), #Cuando la Asignacion es generada
	('1', 'PAGADO'), #Cuando el comprador notifica el pago
	('2', 'PRODUCTO ENVIADO'), #Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
	('3','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
	('4', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
	('5', 'CANCELADO') #Cuando se cancela la transaccion

)



class RequestItem(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by RequestItem")
	price = models.IntegerField()
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=1024)
	quantity = models.IntegerField() 
	######Categoria de los Productos
	itemsCatA = models.ForeignKey(ItemsCatA, help_text="")
	itemsCatB = ChainedForeignKey(
		ItemsCatB,
		chained_field="itemsCatA",
       		chained_model_field="itemsCatA", 
        	show_all=False, 
        	auto_choose=True,
		help_text=""
	)
	itemsCatC = ChainedForeignKey(ItemsCatC, chained_field="itemsCatB", chained_model_field="itemsCatB", help_text = "")
	######Categoria de los Productos
	brand = models.CharField(max_length=25)
	model = models.CharField(max_length=25)
	state = models.CharField(max_length=7, choices=STATES_CHOICES)
	date = models.DateTimeField(auto_now_add=True)
	daysLimit = models.IntegerField()
	pictures = models.ManyToManyField(Picture, through='RequestItemPicture', blank=True)
	addressDelivery = models.CharField(max_length=177)

	def __unicode__(self):
		return u'Title: %s' % (self.title)

	#True si el item ya posee candidatos
	def has_candidates(self):
		if Proffer.objects.filter(requestItem = self).exists():
			return True
		else:
			return False

	#True si el item ya posee asignacion
	def has_assignment(self):
		try:
			Assignment.objects.get(requestItem = self)
		except Assignment.DoesNotExist:
			return False
		return True

	#True si el item ya ha finalizado
	def has_been_completed(self):
		try:
			assignment = Assignment.objects.get(requestItem = self)
		except Assignment.DoesNotExist:
			return False
		if assignment.status == "4":
			return True
		return False

	#Regresa el link de la primer imagen en miniatura 100x100 del item
	def get_first_picture_100x100(self):
		for p in self.pictures.all()[:1]:
			return p.get_url_100x100()

	#Regresa el link de la primer imagen en miniatura 250x250 del item
	def get_first_picture_250x250(self):
		for p in self.pictures.all()[:1]:
			return p.get_url_250x250()

		
class RequestItemPicture(models.Model):
	requestItem = models.ForeignKey(RequestItem)
	picture = models.ForeignKey(Picture)

	def __unicode__(self):
		return u'%s' % (self.requestItem.title)

class Proffer(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Proffer")
	requestItem = models.ForeignKey(RequestItem)
	date = models.DateTimeField(auto_now_add=True)
	cprice = models.IntegerField()
	message = models.CharField(max_length=140)
	pictures = models.ManyToManyField(Picture, through='ProfferPicture')

	def __unicode__(self):
		return u'owner: %s, item: %s' % (self.owner, self.requestItem.title)

	def is_open(self):
		try:
			Assignment.objects.get(requestItem = self.requestItem)
		except Assignment.DoesNotExist:
			return True
		return False

class ProfferPicture(models.Model):
	proffer = models.ForeignKey(Proffer)
	picture = models.ForeignKey(Picture)

	def __unicode__(self):
		return self.proffer

class Assignment(models.Model):
	owner = models.ForeignKey(User)
	requestItem = models.ForeignKey(RequestItem)
	date = models.DateTimeField(auto_now_add=True)
	duedate = models.DateTimeField(null=True, blank=True)
	comment = models.CharField(max_length=144)
	status = models.CharField(max_length=2, default = 0)

	def __unicode__(self):
		return u'Owner: %s and item: %s' % (self.owner, self.requestItem)

	def is_saller(self,user):
		if self.owner == user:
			return True
		else: 
			return False

	def is_buyer(self,user):
		if self.requestItem.owner == user:
			return True
		else:
			return False








