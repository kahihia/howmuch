from howmuch.backend.email import Email

#Si quien postea no esta en followers y no es el comprador
def add_follower(article, user):
	if (user not in article.followers.all()) and (article.owner is not user):
		article.followers.add(user)

#Agregar articulo a la lista de followings del usuario
def add_following(article,user):
	if article not in user.profile.following.all():
		user.profile.following.add(article)

def send_mail_to_followers(article, post):
	subject = 'El comprador ha comentado en el articulo %s' % (article.title)
	context_render = {'article' : article, 'post' : post }
	template = 'emails/comments/send_mail_to_followers.html'
	#Se envia un email a cada stakeholder
	for follower in article.followers.all():
		Email(follower,subject,context_render,template).send()


def send_mail_to_buyer(article, post):
	context_render = {'article' : article, 'post' : post }
	subject = 'Han comentado en el articulo que publicaste %s' % (article.title)
	template = 'emails/comments/send_mail_to_buyer.html'
	#Se envia un mail al comprador
	Email(article.owner ,subject,context_render,template).send()
	pass


def send_mail(article, user, post):
	#Si el comprador comenta, enviar mail a los followers
	if article.owner == user:
		send_mail_to_followers(article, post)
	#Si un follower comenta, enviar mail al comprador
	else:
		send_mail_to_buyer(article, post)


