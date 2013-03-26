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
	invoice = models.CharField(max_length=10)
	period = models.IntegerField(default=1)
	reference = models.CharField(max_length=15, blank=True)
	charges = models.ManyToManyField(Charge)
	total = models.IntegerField(default=0)
	is_paid = models.BooleanField(default=False)
	due_date = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.reference)

	def create_user_invoice(sender, instance, created, **kwargs):
		from howmuch.invoice.functions import generate_reference, generate_number_invoice
		if created:
			invoice = Invoice.objects.create(owner=instance)
			invoice.reference = generate_reference(instance)
			invoice.invoice = generate_number_invoice(invoice.pk)
			invoice.save()


	def get_item_name(self):
		return 'Pago de Factura %s' % (self.invoice)


	post_save.connect(create_user_invoice, sender=User)


class Pay(models.Model):
	from paypal.standard.ipn.models import PayPalIPN

	owner = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	invoice = models.OneToOneField(Invoice)
	amount = models.FloatField()
	reference = models.CharField(max_length=15)

	def __unicode__(self):
		return u'%s' % (self.invoice)

	def create_pay(sender, instance, created, **kwargs):
		from howmuch.invoice.models import Invoice
		
		if created:
			invoice = Invoice.objects.get(invoice=str(instance.invoice))
			pay = Pay.objects.create(invoice=invoice, amount=float(instance.mc_gross), reference=invoice.reference)

	post_save.connect(create_pay, sender=PayPalIPN)




