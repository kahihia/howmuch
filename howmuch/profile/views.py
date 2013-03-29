import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from howmuch.article.models import Article
from howmuch.prestige.models import Critique
from howmuch.profile.forms import ProfileForm, AddressForm, PhoneForm, AccountBankForm
from howmuch.profile.functions import add_following, remove_following
from howmuch.profile.models import Profile, Address, Phone, AccountBank


@login_required(login_url="/login")
def view_profile(request, username):
    profile = get_object_or_404(Profile, user__username = username)
    return render_to_response('profile/viewProfile.html', {'profile' : profile}, 
        context_instance=RequestContext(request))


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
    return render_to_response('profile/edit.html', {'form' : form }, 
        context_instance=RequestContext(request))

@login_required(login_url="/login/")
def new_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            newAddress = form.save(commit=False)
            newAddress.owner = request.user
            newAddress.save()
            request.user.profile.addresses.add(newAddress)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AddressForm()
    return render_to_response('profile/newAddress.html', {'form' : form}, 
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def edit_address(request, addressID):
    current = get_object_or_404(Address, pk=addressID, owner = request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=current)
        if form.is_valid():
            address = form.save()
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AddressForm(instance=current)
    return render_to_response('profile/newAddress.html', {'form':form},
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def delete_address(request,addressID):
    address = get_object_or_404(Address, pk=addressID, owner=request.user)
    address.delete()
    return HttpResponseRedirect('/profile/e/edit')

@login_required(login_url='/login/')
def new_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            newPhone = form.save(commit=False)
            newPhone.owner = request.user
            newPhone.save()
            request.user.profile.phones.add(newPhone)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = PhoneForm()
    return render_to_response('profile/newPhone.html', {'form' : form}, 
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def edit_phone(request, phoneID):
    current = get_object_or_404(Phone, pk=phoneID, owner=request.user)

    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=current)
        if form.is_valid():
            phone = form.save()
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = PhoneForm(instance=current)
    return render_to_response('profile/newPhone.html', {'form':form},
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def delete_phone(request, phoneID):
    phone = get_object_or_404(Phone, pk=phoneID, owner=request.user)
    phone.delete()
    return HttpResponseRedirect('/profile/e/edit')


@login_required(login_url='/login/')
def new_account_bank(request):
    if request.method == 'POST':
        form = AccountBankForm(request.POST)
        if form.is_valid():
            newAccountBank = form.save(commit=False)
            newAccountBank.owner = request.user
            newAccountBank.save()
            request.user.profile.banks.add(newAccountBank)
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AccountBankForm()
    return render_to_response('profile/newAccountBank.html', {'form' : form }, 
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def edit_account_bank(request, bankID):
    current = get_object_or_404(AccountBank, pk=bankID, owner=request.user)

    if request.method == 'POST':
        form = AccountBankForm(request.POST, instance=current)
        if form.is_valid():
            bank = form.save()
            return HttpResponseRedirect('/profile/e/edit')
    else:
        form = AccountBankForm(instance=current)
    return render_to_response('profile/newAccountBank.html', {'form':form},
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
def delete_account_bank(request, bankID):
    bank = get_object_or_404(AccountBank, pk=bankID, owner=request.user)
    bank.delete()
    return HttpResponseRedirect('/profile/e/edit')

@login_required(login_url='/login/')
def following(request):
    return render_to_response('profile/following.html', {'following' : request.user.profile.following.all()},
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def follow(request, articleID):
    article = get_object_or_404(Article, pk=articleID)
    add_following(article,request.user)
    return HttpResponse(json.dumps({'response' : 'siguiendo'}))

@login_required(login_url='/login/')
def unfollow(request,articleID):
    article = get_object_or_404(Article, pk=articleID)
    remove_following(article, request.user)
    return HttpResponse(json.dumps({'response' : 'lo dejaste de seguir' }))


@login_required(login_url='/login/')
def first_time(request):
    from howmuch.profile.functions import change_status_first_time

    change_status_first_time(request.user)
    return HttpResponse('Gracias')

@login_required(login_url='/login')
def first_post(request):
    from howmuch.profile.functions import change_status_first_post

    change_status_first_post(request.user)
    return HttpResponse('Gracias')






    







    



