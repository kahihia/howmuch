from howmuch.core.forms import RequestItemForm
from howmuch.core.models import RequestItem
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta, date
from django.template import RequestContext
import datetime

@login_required(login_url="/login/")
def home(request):
	return render_to_response('core/home.html', context_instance=RequestContext(request))


@login_required(login_url="/login/")
def requestItem(request):
	if request.method == 'GET':
		title = "Pago $ " + request.GET['precio'] + " Por " + request.GET['descripcion'] 
	if request.method == 'POST':
		form = RequestItemForm(request.POST)
		if form.is_valid():
			newItem = form.save(commit=False)
			newItem.owner = request.user
			newItem.save()
			return HttpResponseRedirect('/thanks/')
	else:
		form = RequestItemForm(initial={'title' : title, 'price' : request.GET['precio'], 'addressDelivery' : request.user.get_profile().getAddressDelivery()})
	return render_to_response('core/newitem.html', {'form' : form}, context_instance=RequestContext(request))

