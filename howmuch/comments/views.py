from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from howmuch.comments.models import Comment
from howmuch.comments.forms import CommentForm
from howmuch.comments.functions import send_mail
from howmuch.profile.functions import add_follower, add_following
from howmuch.article.models import Article

@login_required(login_url="/login/")
def post(request, articleID):
	article = get_object_or_404(Article, pk=articleID)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.owner = request.user
			post.save()
			article.comments.add(post)
			#add follower
			add_follower(article, request.user)
			#add following
			add_following(article, request.user)
			#Send email to buyer or followers
			send_mail(article, request.user, post)
			#html content for http response
			html_content = "<div class='question group'>" +\
			"<div class='question-profile-picture width-10 float-left'>" +\
			"<div class='container padding-0_5em'>" +\
			"<img class='width-100' src='%s'/>" % (post.owner.profile.get_profile_picture()) +\
			"</div>" +\
			"</div>" +\
			"<div class='question-content width-90 float-right'>" +\
			"<div class='container padding-0_5em'>" +\
			"<div class='question-user-name'>" +\
			"<a class='strong attention' href='#'>%s</a>" % (post.owner) +\
			"</div>" +\
			"<div class='question-info'>" +\
			"%s" % (post.comment) +\
			"</div>" +\
			"<div class='question-published text-align-right'>" +\
			"hace %s" % (post.get_timestamp()) +\
			"</div>" +\
			"</div>" +\
			"</div>" +\
			"</div>" 

			return HttpResponse(html_content)




