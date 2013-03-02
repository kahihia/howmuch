def update_prestige(user):
    if user.total_points() < 100:
        user.profile.prestige = 'Sirius'
        user.profile.save()
    elif user.total_points() > 100 and user.total_points() < 500:
        user.profile.prestige = 'Antares'
        user.profile.save()
    elif user.total_points() > 500 and user.total_points() < 2000:
        user.profile.prestige = 'Mu Cephei'
        user.profile.save()
    elif user.total_points() > 2000:
        user.profile.prestige = 'Canis Majoris'
        user.profile.save()


def add_points(user, points):
    user.profile.positive_points += points
    user.profile.save()
    

def remove_points(user,points):
    user.profile.negative_points += points
    user.profile.save()

def get_more_populars():
    pass








    

