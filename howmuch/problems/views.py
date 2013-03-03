from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q

from howmuch.article.models import Assignment
from howmuch.problems.forms import ProblemForm, ProblemOutForm ,ReplyForm, ActionForm
from howmuch.problems.models import Problem

@login_required(login_url='/login/')
def problem(request, assignmentID):
	assignment = get_object_or_404(Assignment, pk=assignmentID)
	if request.method == 'POST':
		form = ProblemForm(request.POST)
		if form.is_valid():
			problem  = form.save(commit=False)
			problem.owner = request.user
			problem.assignment = assignment
			problem.save()
			return HttpResponse('Hemos recibido tu solicutud, enseguida nos comunicaremos contigo')
	else:
		form = ProblemForm()
	return render_to_response('problems/problem.html', {'form' : form }, 
		context_instance=RequestContext(request))

@login_required(login_url='/login/')
def problem_out(request):
	#Asignaciones donde el usuario es ya sea comprador o vendedor
	queryset = Assignment.objects.filter(Q(owner=request.user) | Q(article__owner=request.user))
	if request.method == 'POST':
		form = ProblemOutForm(request.POST)
		if form.is_valid():
			problem = form.save(commit=False)
			problem.owner = request.user
			problem.save()
			return HttpResponse('Hemos recibido tu solicitud, enseguida nos comunicaremos contigo')
	else:
		form = ProblemOutForm()
		form.fields['assignment'].queryset = queryset
	return render_to_response('problems/problem_out.html',{'form':form}, 
		context_instance=RequestContext(request))


@login_required(login_url='/login/')
def reply(request, problemID):
	#Validar que solo un Admin pueda responder el Problema
	problem = get_object_or_404(Problem, pk=problemID)
	if request.method == 'POST':
		form = ReplyForm(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.admin = request.user
			reply.problem = problem
			reply.save()
			return HttpResponse('Has respondido el Problema')
	else:
		form = ReplyForm()
	return render_to_response('problems/reply.html', {'form' : form }, 
		context_instance=RequestContext(request))


@login_required(login_url='/login/')
def action(request, problemID):
	problem = get_object_or_404(Problem, pk=problemID)
	if request.method == 'POST':
		form = ActionForm(request.POST)
		if form.is_valid():
			action = form.save(commit=False)
			action.problem = problem
			action.save()
			return HttpResponse('Has tomado una accion para este problema')
	else:
		form = ActionForm()
	return render_to_response('problems/action.html', {'form' : form },
		context_instance=RequestContext(request))


@login_required(login_url='/login/')
def my_problems(request):
	problems = Problem.objects.filter(owner=request.user)
	return render_to_response('problems/my_problems.html', {'problems' : problems }, 
		context_instance=RequestContext(request))
