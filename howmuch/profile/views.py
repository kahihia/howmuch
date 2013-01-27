from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from howmuch.profile.forms import ProfileForm, AddressForm, PhoneForm, AccountBankForm
from howmuch.profile.models import Profile
from howmuch.prestige.models import PrestigeLikeBuyer, PrestigeLikeSeller


@login_required(login_url="/login")
def viewProfile(request, username):
    prestigeLikeBuyer = PrestigeLikeBuyer.objects.filter(to__username = username).order_by('date')[:10]
    prestigeLikeSeller = PrestigeLikeSeller.objects.filter(to__username = username).order_by('date')[:10]
    profile = get_object_or_404(Profile, user__username = username)

    return render_to_response('profile/viewProfile.html', {'prestigeLikeBuyer' : prestigeLikeBuyer,
        'prestigeLikeSeller' : prestigeLikeSeller, 'profile' : profile}, context_instance=RequestContext(request))


@login_required(login_url="/login")
def edit(request):
    current = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES ,instance=current)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/profile/e/edit/")
    else:
        form =ProfileForm(instance=current)
    return render_to_response('profile/edit.html', {'form' : form }, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def newAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            newAddress = form.save()
            request.user.profile.addresses.add(newAddress)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AddressForm()
    return render_to_response('profile/newAddress.html', {'form' : form}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def newPhone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            newPhone = form.save()
            request.user.profile.phones.add(newPhone)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = PhoneForm()
    return render_to_response('profile/newPhone.html', {'form' : form}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def newAccountBank(request):
    if request.method == 'POST':
        form = AccountBankForm(request.POST)
        if form.is_valid():
            newAccountBank = form.save()
            request.user.profile.banks.add(newAccountBank)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AccountBankForm()
    return render_to_response('profile/newAccountBank.html', {'form' : form }, context_instance=RequestContext(request))


    







    



