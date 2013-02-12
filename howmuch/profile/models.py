from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from django_facebook.models import FacebookProfileModel

from howmuch.pictures.models import make_upload_path
from howmuch.pictures.thumbs import ImageWithThumbsField

PHONE_CHOICES =(

    ('1','Casa'),
    ('2','Trabajo'),
    ('3', 'Celular'),

    )

class Address(models.Model):
    street = models.CharField(max_length = 100)
    number = models.CharField(max_length = 10)
    suburb = models.CharField(max_length = 100)
    city = models.CharField(max_length = 33)
    state = models.CharField(max_length = 33)
    country = models.CharField(max_length = 33)
    zipcode = models.IntegerField()

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s' % (self.street, self.number, self.suburb, self.city, self.state, self.country, self.zipcode)

    def get_address(self):
        return 'Calle %s, Numero %s, Colonia %s, %s, %s, %s, C.P %s' % (self.street, self.number, self.suburb, self.city, self.state, self.country, self.zipcode)

class Phone(models.Model):
    place = models.CharField(max_length=20,choices=PHONE_CHOICES)
    number = models.BigIntegerField()

    def __unicode__(self):
        return u'%s' % (self.number)

class AccountBank(models.Model):
    bank = models.CharField(max_length=20)
    account = models.CharField(max_length=33)

    def __unicode__(self):
        return u'%s %s' % (self.bank, self.account)

class Profile(FacebookProfileModel):
    user = models.OneToOneField(User)
    profile_picture = ImageWithThumbsField(upload_to=make_upload_path, sizes=((50,50),(100,100),(250,250)) )
    company = models.CharField(max_length=77, null = True, blank=True)
    addresses = models.ManyToManyField(Address, blank = True)
    phones = models.ManyToManyField(Phone, blank = True)
    banks = models.ManyToManyField(AccountBank, blank = True)
    total_purchases = models.IntegerField(default = 0)
    total_sales = models.IntegerField(default = 0)
    prestige = models.CharField(max_length=1, default = 'A')
    unread_notifications = models.IntegerField(default = 0)
    unread_conversations = models.IntegerField(default = 0)

    def __unicode__(self):
        return u'%s' % (self.user)

#Se crea el perfil del usuario en el momento que se crea al usuario
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def add_unread_notification(self):
        self.unread_notifications += 1
        self.save()

    def remove_unread_notification(self):
        self.unread_notifications -= 1
        self.save()

    def add_unread_conversation(self):
        self.unread_conversations += 1
        self.save()

    def remove_unread_conversation(self):
        self.unread_conversations -= 1
        self.save()

    def add_purchases(self):
        self.total_purchases += 1
        self.save()

    def add_sales(self):
        self.total_sales += 1
        self.save()

    def get_profile_picture_50x50(self):
        return str(self.profile_picture.url_50x50).split("?")[0]

    def get_profile_picture_100x100(self):
        return str(self.profile_picture.url_100x100).split("?")[0]

    def get_profile_picture_250x250(self):
        return str(self.profile_picture.url_250x250).split("?")[0]

    def get_banks(self):
        banks = ''
        for bank in self.banks.all():
            banks += 'Banco: %s, Cta: %s. ' % (bank.bank, bank.account)
        return str(banks)









