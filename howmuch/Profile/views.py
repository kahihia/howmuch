from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from howmuch.Profile.forms import ProfileForm
from howmuch.Profile.models import Profile

@login_required(login_url="/login")
def edit(request):
	current = get_object_or_404(Profile, user=request.user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=current)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/profile/edit/")
	else:
		form =ProfileForm(instance=current)
	return render_to_response('profile/editprofile.html', {'form' : form }, context_instance=RequestContext(request))



