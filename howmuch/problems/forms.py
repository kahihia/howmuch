from django.forms import ModelForm, Textarea

from howmuch.problems.models import Problem, Reply, Action

class ProblemForm(ModelForm):
	class Meta:
		model = Problem
		exclude = ('owner', 'assignment', 'date', 'is_solved', 'status')
		widgets = {
			'description' : Textarea(attrs={'class' : 'span11'})
		}


class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		exclude = ('admin', 'problem', 'date')


class ActionForm(ModelForm):
	class Meta:
		model = Action
		exclude = ('problem', 'date')