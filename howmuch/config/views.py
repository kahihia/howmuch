from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from howmuch.config.forms import NotificationsConfigForm, EmailChangeForm
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

@login_required(login_url='/login/')
def change_email(request,
                 post_change_redirect='/config/notifications/',
                 template_name='config/change_email.html'):
    if request.method == 'POST':
        form = EmailChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            change_email = form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = EmailChangeForm(user=request.user)
    return render_to_response(template_name, {'form' : form}, 
        context_instance =RequestContext(request))

