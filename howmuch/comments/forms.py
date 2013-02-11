from django.forms import ModelForm

from howmuch.comments.models import Comment

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('owner', 'date', )