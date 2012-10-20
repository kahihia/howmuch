from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from howmuch.perfil.forms import PerfilForm
from howmuch.perfil.models import Perfil

@login_required(login_url="/login")
def edit(request):
	current = get_object_or_404(Perfil, user=request.user)
	if request.method == 'POST':
		form = PerfilForm(request.POST, request.FILES ,instance=current)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/profile/edit/")
	else:
		form =PerfilForm(instance=current)
	return render_to_response('profile/editprofile.html', {'form' : form }, context_instance=RequestContext(request))



