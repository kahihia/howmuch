# -*- encoding: utf-8 -*-
from howmuch.pictures.forms import PictureForm
from howmuch.core.models import RequestItem, RequestItemPicture, Proffer, ProfferPicture
from howmuch.pictures.models import Picture
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect


def addPictureProffer(request, profferID):
    #Validar que exista la Propuesta y que el usuario sea el dueño de la misma
    proffer = get_object_or_404(Proffer, pk= profferID, owner = request.user)
    pictures = proffer.pictures.all()

    if request.method == 'POST':
        form = PictureForm(request.POST,request.FILES)
        if form.is_valid():
            newPicture = form.save(commit = False)
            newPicture.owner = request.user
            newPicture.save()
            #Se crea un objeto de la clase ProfferPicture
            newProfferPicture = ProfferPicture(proffer = proffer, picture = newPicture)
            newProfferPicture.save()
            return HttpResponseRedirect("/pictures/addpicture/proffer/" + profferID)
    else:
        form = PictureForm()
    return render_to_response('pictures/addPicture.html', {'form' : form, 'pictures' : pictures }, context_instance = RequestContext(request))


def addPictureRequestItem(request, requestItemID):
    #Validar que exista el RequestItem y que el usuario sea el owner de la misma
    requestItem = get_object_or_404(RequestItem, pk = requestItemID, owner = request.user)
    pictures = requestItem.pictures.all()

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            newPicture = form.save(commit = False)
            newPicture.owner = request.user
            newPicture.save()
            #Se crea un objeto de la clase RequestItemPicture
            newRequestItemPicture = RequestItemPicture(requestItem = requestItem, picture = newPicture)
            newRequestItemPicture.save()
            return HttpResponseRedirect("/pictures/addpicture/requestitem/" + requestItemID )
    else:
        form = PictureForm()
    return render_to_response('pictures/addPicture.html', {'form' : form, 'pictures' : pictures }, context_instance = RequestContext(request))



