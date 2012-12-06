from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from howmuch.config.forms import NotificationsConfigForm
from howmuch.config.models import NotificationsConfig

@login_required(login_url='/login/')
def edit_config(request):
    current = get_object_or_404(NotificationsConfig, user = request.user )
    if request.method == 'POST':
        form = NotificationsConfigForm(request.POST, instance = current )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        form = NotificationsConfigForm(instance=current)
    return render_to_response('config/editConfig.html', {'form' : form }, context_instance = RequestContext(request))

