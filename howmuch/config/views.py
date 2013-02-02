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
            return HttpResponseRedirect('' + '?save_changes=True')
    else:
        form = NotificationsConfigForm(instance=current)
    if request.GET.__contains__('save_changes') and request.GET['save_changes']:
    	save_changes = True
    else:
    	save_changes = False
    return render_to_response('config/config.html', {'form' : form, 'save_changes' : save_changes}, 
    	context_instance = RequestContext(request))

