# -*- encoding: utf-8 -*-
from howmuch.pictures.forms import PictureForm
from howmuch.core.models import Proffer, ProfferPicture
from howmuch.pictures.models import Picture
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse


def addPicture(request, profferID):
	#Validar que exista la Propuesta y que el usuario sea el dueño de la misma
	proffer = get_object_or_404(Proffer, pk= profferID, owner = request.user)

	if request.method == 'POST':
		form = PictureForm(request.POST,request.FILES)
		if form.is_valid():
			newPicture = form.save(commit = False)
			newPicture.owner = request.user
			newPicture.save()
			#Se crea un objeto de la clase ProfferPicture
			newProfferPicture = ProfferPicture(proffer = proffer, picture = newPicture)
			newProfferPicture.save()
			return HttpResponse("Imagen Subida Correctamente")
	else:
		form = PictureForm()
	return render_to_response('pictures/addPicture.html', {'form' : form }, context_instance = RequestContext(request))



