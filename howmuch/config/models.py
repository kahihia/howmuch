from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class NotificationsConfig(models.Model):
    user = models.OneToOneField(User)
    new_offer = models.BooleanField(default=True)
    new_sale = models.BooleanField(default=True)
    new_message = models.BooleanField(default=True)
    confirm_pay = models.BooleanField(default=True)
    confirm_delivery = models.BooleanField(default=True)
    new_critique = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.user)

    """
    Cuando se crea el nuevo usuario tambien se crea su configuracion de notificaciones
    """
    def create_user_config(sender, instance, created, **kwargs):
        if created:
            NotificationsConfig.objects.create(user=instance)

    post_save.connect(create_user_config, sender=User)

