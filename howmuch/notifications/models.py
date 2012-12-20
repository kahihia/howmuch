# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from howmuch.backend.functions import get_timestamp
from howmuch.core.models import RequestItem
from django.db.models.signals import post_save


TYPE_CHOICES = (

    ('proffer','Tienes un nuevo Candidato'),
    ('assignment','Has sido seleccionado'),
    ('confirm_pay','Te han confirmado el pago'),
    ('confirm_delivery','Te han confirmado el envio'),
    ('critique','Has sido criticado'),

    )

class Notification(models.Model):
    owner = models.ForeignKey(User)
    requestItem = models.ForeignKey(RequestItem)
    tipo = models.CharField(max_length=20)
    title = models.CharField(max_length=140)
    has_been_readed = models.BooleanField(default=False)
    redirect = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now_add = True)
    idBack = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_timestamp(self):
        return get_timestamp(self.date)



