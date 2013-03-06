from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from howmuch.article.models import Assignment

class Charge(models.Model):
	owner = models.ForeignKey(User)
	period = models.IntegerField()
	assignment = models.OneToOneField(Assignment)
	date = models.DateField(auto_now_add=True)
	price =  models.IntegerField()
	commission = models.IntegerField(default=0)

	def __unicode__(self):
		return u'%s' % (self.assignment.article.title)

class Invoice(models.Model):
	owner = models.ForeignKey(User)
	period = models.IntegerField(default=1)
	reference = models.CharField(max_length=10, blank=True)
	charges = models.ManyToManyField(Charge)
	total = models.IntegerField(default=0)
	is_paid = models.BooleanField(default=False)
	due_date = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.reference)

	def create_user_invoice(sender, instance, created, **kwargs):
		if created:
			Invoice.objects.create(owner=instance)

	post_save.connect(create_user_invoice, sender=User)


class Pay(models.Model):
	owner = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	invoice = models.OneToOneField(Invoice)
	amount = models.IntegerField()
	reference = models.CharField(max_length=10)

	def __unicode__(self):
		return u'%s' % (self.invoice)



