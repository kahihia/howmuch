from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Perfil(models.Model):
	user = models.OneToOneField(User)
	company = models.CharField(max_length=77, null = True, blank=True)
	address = models.CharField(max_length=77)
	address2 = models.CharField(max_length=77, null = True, blank=True)
	city = models.CharField(max_length=17)
	zipcode = models.IntegerField(null = True, blank=True)
	state = models.CharField(max_length=17)
	phone = models.IntegerField(null = True, blank=True)
	bank = models.CharField(max_length=17, null = True, blank=True)
	account_bank = models.CharField(max_length=27, null = True, blank=True)
	account_paypal = models.CharField(max_length=37, null = True, blank=True)

	def __unicode__(self):
		return u'%s' % (self.user)

	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Perfil.objects.create(user=instance)
	post_save.connect(create_user_profile, sender=User)

	def getAddressDelivery(self):
		return self.address + " " + self.city + " " + self.state + " C.P " + str(self.zipcode)

	def isComplete(self):
		return 0
