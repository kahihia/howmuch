from django.db import models
from django.contrib.auth.models import User

from howmuch.utils import get_timestamp
from howmuch.article.models import Article

TYPE_CHOICES = (
    ('offer','Tienes un nuevo Candidato'),
    ('assignment','Has sido seleccionado'),
    ('confirm_pay','Te han confirmado el pago'),
    ('confirm_delivery','Te han confirmado el envio'),
    ('critique','Has sido criticado'),
    )

class Notification(models.Model):
    owner = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    notif_type = models.CharField(max_length=20)
    title = models.CharField(max_length=140)
    has_been_readed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_timestamp(self):
        return get_timestamp(self.date)

    def get_url(self):
        if self.notif_type == 'offer':
            return '/article/candidates/%s?notif_id=%s' % (self.article.pk, self.pk)
        elif self.notif_type == 'assignment':
            return '/messages/%s?notif_id=%s' % (self.article.assignment.conversation.pk, self.pk)
        else:
            return '/messages/%s?notif_id=%s' % (self.article.assignment.conversation.pk, self.pk)





        




