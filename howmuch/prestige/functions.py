from howmuch.prestige.models import PrestigeLikeBuyer, PrestigeLikeSeller
from howmuch.perfil.models import Perfil

def get_prestige_user(user):
	totalCritiquesLikeSeller = PrestigeLikeSeller.objects.filter(to = user).count()
	totalCritiquesLikeBuyer = PrestigeLikeBuyer.objects.filter(to = user).count()

	if totalCritiquesLikeSeller > 0:
		prestigeLikeSeller = (float(PrestigeLikeSeller.objects.filter(to = user, prestige = 'Excelente').count()) / totalCritiquesLikeSeller ) * 100
	else: 
		prestigeLikeSeller = 0

	if totalCritiquesLikeBuyer > 0:
		prestigeLikeBuyer = ( float(PrestigeLikeBuyer.objects.filter(to = user, prestige = 'Excelente').count()) / totalCritiquesLikeBuyer ) * 100
	else: 
		prestigeLikeBuyer = 0

	if prestigeLikeSeller or prestigeLikeBuyer == 0:
		prestigeUser = prestigeLikeSeller + prestigeLikeBuyer
	else:
		prestigeUser = ( (totalCritiquesLikeSeller * prestigeLikeSeller)  +  (totalCritiquesLikeBuyer * prestigeLikeBuyer) ) / (totalCritiquesLikeSeller + totalCritiquesLikeBuyer)

	return prestigeUser

def update_prestige(user):
	prestigeUser = get_prestige_user(user)
	perfilUser = Perfil.objects.get(user = user )

	if prestigeUser >= 0 and prestigeUser < 25:
		perfilUser.prestige = 'A'
		perfilUser.save()
	elif prestigeUser >=25 and prestigeUser < 50:
		perfilUser.prestige = 'B'
		perfilUser.save()
	elif prestigeUser >=50  and prestigeUser < 75:
		perfilUser.prestige = 'C'
		perfilUser.save()
	elif prestigeUser >=75:
		perfilUser.prestige = 'D'
		perfilUser.save()


	

