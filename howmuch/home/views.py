from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from endless_pagination.decorators import page_template

from howmuch.article.models import Article

@login_required(login_url="/login/")
#Decorador requerido para la app de paginacion
@page_template('home/home_index_page.html')
def home(
        request, template='home/home_index.html', extra_context=None):
    context = {
        'items': Article.objects.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))
