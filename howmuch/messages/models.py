# -*- coding: utf8 -*- 

from django.db import models
from howmuch.core.models import Assignment
from howmuch.backend.functions import get_timestamp
from django.contrib.auth.models import User
import datetime

STATUS_CHOICES = (

	('0', 'CLOSED'),
	('1', 'OPEN'),

	)

class Conversation(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	assignment = models.OneToOneField(Assignment)
	status = models.CharField(max_length=2, default = "1")

	def __unicode__(self):
		return u'Assignment to: %s ' % (self.assignment.requestItem)

	def get_latest_message(self):
		messages =  Message.objects.filter(conversation=self).order_by('-date')[:1]
		for message in messages:
			return message

	def is_buyer(self,user):
		if self.assignment.requestItem.owner == user:
			return True
		return False

	def is_seller(self,user):
		if self.assignment.owner == user:
			return True
		return False

	def user_inside(self,user):
		if self.is_buyer(user) or self.is_seller(user):
			return True
		return False

	"""
	Mensajes sin leer para el buyer
	"""
	def getNumber_unread_messages_buyer(self):
		return Message.objects.filter(owner = self.assignment.owner , conversation=self, has_been_readed=False).count()

	"""
	Mensajes sin leer para el seller
	"""
	def getNumber_unread_messages_seller(self):
		return Message.objects.filter(owner= self.assignment.requestItem.owner , conversation=self, has_been_readed=False).count()

	def has_unread_messages(self):
		if self.getNumber_unread_messages_seller() > 0 or self.getNumber_unread_messages_buyer() > 0:
			return True
		return False



class Message(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Message")
	date = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length=250)
	has_been_readed = models.BooleanField(default=False)
	conversation = models.ForeignKey(Conversation)

	def __unicode__(self):
		return u'message: %s' % (self.message)

	def get_timestamp(self):
		return get_timestamp(self.date)

