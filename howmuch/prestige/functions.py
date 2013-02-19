from howmuch.prestige.models import PrestigeLikeBuyer, PrestigeLikeSeller
from howmuch.profile.models import Profile

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
    profileUser = Profile.objects.get(user = user )

    if prestigeUser >= 0 and prestigeUser < 25:
        profileUser.prestige = 'Sirius'
        profileUser.save()
    elif prestigeUser >=25 and prestigeUser < 50:
        profileUser.prestige = 'Antares'
        profileUser.save()
    elif prestigeUser >=50  and prestigeUser < 75:
        profileUser.prestige = 'Mu Cephei'
        profileUser.save()
    elif prestigeUser >=75:
        profileUser.prestige = 'Canis Majoris'
        profileUser.save()


    

