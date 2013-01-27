from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from howmuch.config.forms import NotificationsConfigForm
from howmuch.config.models import Notifications

@login_required(login_url='/login/')
def notifications_config(request):
    current = get_object_or_404(Notifications, user = request.user )
    if request.method == 'POST':
        form = NotificationsConfigForm(request.POST, instance = current )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        form = NotificationsConfigForm(instance=current)
    return render_to_response('config/config.html', {'form' : form }, context_instance = RequestContext(request))

