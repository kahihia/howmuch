from django.contrib import admin
from howmuch.profile.models import Profile, Address, Phone, AccountBank

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(AccountBank)
