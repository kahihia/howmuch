from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (

	('1','Tienes un nuevo Candidato'),
	('2','Has sido seleccionado'),
	('3','Te han confirmado el pago'),
	('4','Te han confirmado el envio'),
	('5','Has sido criticado'),

	)

class Notification(models.Model):
	owner = models.ForeignKey(User)
	tipo = models.CharField(max_length=1)
	title = models.CharField(max_length=140)
	has_been_readed = models.BooleanField(default=False)
	redirect = models.CharField(max_length=140)
	date = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return u'%s' % (self.title)



