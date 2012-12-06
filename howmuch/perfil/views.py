from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from howmuch.perfil.forms import PerfilForm, AddressForm, PhoneForm, AccountBankForm
from howmuch.perfil.models import Perfil
from howmuch.prestige.models import PrestigeLikeBuyer, PrestigeLikeSeller



def viewProfile(request, username):
    prestigeLikeBuyer = PrestigeLikeBuyer.objects.filter(to__username = username).order_by('date')[:10]
    prestigeLikeSeller = PrestigeLikeSeller.objects.filter(to__username = username).order_by('date')[:10]
    perfil = get_object_or_404(Perfil, user__username = username)


    return render_to_response('profile/viewProfile.html', {'prestigeLikeBuyer' : prestigeLikeBuyer,
        'prestigeLikeSeller' : prestigeLikeSeller, 'perfil' : perfil}, context_instance=RequestContext(request))


@login_required(login_url="/login")
def edit(request):
    current = get_object_or_404(Perfil, user=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES ,instance=current)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/profile/e/edit/")
    else:
        form =PerfilForm(instance=current)
    return render_to_response('profile/editprofile.html', {'form' : form }, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def newAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            newAddress = form.save()
            request.user.perfil.addresses.add(newAddress)
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
            request.user.perfil.phones.add(newPhone)
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
            request.user.perfil.banks.add(newAccountBank)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AccountBankForm()
    return render_to_response('profile/newAccountBank.html', {'form' : form }, context_instance=RequestContext(request))


    







    



