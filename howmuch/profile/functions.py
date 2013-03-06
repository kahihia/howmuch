from howmuch.invoice.models import Invoice

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

"""
La funcion bloquear usuario debe ser llamada todos los dias y consiste
en validar para cada usuario si ya excedio su fecha limite de pago, en caso que si,
se procede a bloquear la cuenta del usuario, los usuarios con cuentas bloqueadas
no podran publicar articulos ni realizar ofertas a compradores
"""

def block_user(user):
	import datetime
	current_invoice = Invoice.objects.get(owner=user, period = user.profile.current_invoice)
	if current_invoice.is_paid == False and current_invoice.due_date > datetime.date.now():
		user.profile.is_block = True
		user.profile.save()

