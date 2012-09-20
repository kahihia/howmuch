from howmuch.core.forms import RequestItemForm
from howmuch.core.models import RequestItem
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta, date
from django.template import RequestContext
import datetime