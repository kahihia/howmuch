#Si quien postea no esta en followers y no es el comprador
def add_follower(article, user):
	if (user not in article.followers.all()) and (article.owner is not user):
		article.followers.add(user)

#Agregar articulo a la lista de followings del usuario
def add_following(article, user):
	if article not in user.profile.following.all():
		user.profile.following.add(article)

#Quitar articulo a la lista de followings del usuario
def remove_following(article, user):
	if article in user.profile.following.all():
		user.profile.following.remove(article)