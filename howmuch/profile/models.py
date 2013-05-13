from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from django_facebook.models import FacebookProfileModel

from howmuch.pictures.models import make_upload_path
from howmuch.settings import PRESTIGE_TYPES

PHONE_CHOICES =(

    ('1','Casa'),
    ('2','Trabajo'),
    ('3', 'Celular'),

    )

class Address(models.Model):
    owner = models.ForeignKey(User)
    street = models.CharField(max_length = 100)
    number = models.CharField(max_length = 10)
    suburb = models.CharField(max_length = 100)
    city = models.CharField(max_length = 33)
    state = models.CharField(max_length = 33)
    country = models.CharField(max_length = 33)
    zipcode = models.IntegerField()

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s' % (self.street, self.number, self.suburb, self.city, 
            self.state, self.country, self.zipcode)

    def get_address(self):
        return 'Calle %s, Numero %s, Colonia %s, %s, %s, %s, C.P %s' % (self.street, self.number, self.suburb, 
            self.city, self.state, self.country, self.zipcode)

class Phone(models.Model):
    owner = models.ForeignKey(User)
    place = models.CharField(max_length=20,choices=PHONE_CHOICES)
    number = models.BigIntegerField()

    def __unicode__(self):
        return u'%s' % (self.number)

class AccountBank(models.Model):
    owner = models.ForeignKey(User)
    bank = models.CharField(max_length=20)
    account = models.CharField(max_length=33)

    def __unicode__(self):
        return u'%s %s' % (self.bank, self.account)

class Profile(FacebookProfileModel):
    from howmuch.article.models import Article

    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to=make_upload_path, default = '/media/img/cuantoo_profile_picture.png')
    company = models.CharField(max_length=77, null = True, blank=True)
    is_new = models.BooleanField(default=True)
    is_his_first_post = models.BooleanField(default=True)
    following = models.ManyToManyField(Article, blank = True)
    addresses = models.ManyToManyField(Address, blank = True)
    phones = models.ManyToManyField(Phone, blank = True)
    banks = models.ManyToManyField(AccountBank, blank = True)
    total_purchases = models.IntegerField(default = 0)
    total_sales = models.IntegerField(default = 0)
    prestige = models.CharField(max_length=15, default = PRESTIGE_TYPES['PRESTIGE1']['NAME'])
    positive_points = models.IntegerField(default=0)
    negative_points = models.IntegerField(default=0)
    unread_notifications = models.IntegerField(default = 0)
    unread_conversations = models.IntegerField(default = 0)
    current_invoice = models.IntegerField(default = 1)
    credit_limit = models.IntegerField(default=PRESTIGE_TYPES['PRESTIGE1']['LIMIT'])
    is_block = models.BooleanField(default=False)


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

    def get_profile_picture(self):
        return str(self.profile_picture.url).split("?")[0]


    def get_banks(self):
        banks = ''
        for bank in self.banks.all():
            banks += 'Banco: %s, Cta: %s. ' % (bank.bank, bank.account)
        return str(banks)

    #Return total points 
    def total_points(self):
        return self.positive_points - self.negative_points

    #Return current invoice of user
    def get_current_invoice(self):
        from howmuch.invoice.models import Invoice

        current_invoice = Invoice.objects.get(owner=self.user, 
            period=self.current_invoice)
        return current_invoice

    #Return progress profile 
    def get_profile_progress(self):
        progress = 25
        if self.addresses.exists():
            progress += 25
        if self.phones.exists():
            progress += 25
        if self.banks.exists():
            progress +=25
        return progress








