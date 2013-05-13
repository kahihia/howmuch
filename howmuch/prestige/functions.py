from howmuch.settings import PRESTIGE_TYPES

def update_prestige(user):
    if user.profile.total_points() in PRESTIGE_TYPES['PRESTIGE1']['INTERVAL']:
        user.profile.prestige = PRESTIGE_TYPES['PRESTIGE1']['NAME']
        user.profile.credit_limit = PRESTIGE_TYPES['PRESTIGE1']['LIMIT']
        user.profile.save()
    elif user.profile.total_points() in PRESTIGE_TYPES['PRESTIGE2']['INTERVAL']:
        user.profile.prestige = PRESTIGE_TYPES['PRESTIGE2']['NAME']
        user.profile.credit_limit = PRESTIGE_TYPES['PRESTIGE2']['LIMIT']
        user.profile.save()
    elif user.profile.total_points() in PRESTIGE_TYPES['PRESTIGE3']['INTERVAL']:
        user.profile.prestige = PRESTIGE_TYPES['PRESTIGE3']['NAME']
        user.profile.credit_limit = PRESTIGE_TYPES['PRESTIGE3']['LIMIT']
        user.profile.save()
    elif user.profile.total_points() in PRESTIGE_TYPES['PRESTIGE4']['INTERVAL']:
        user.profile.prestige = PRESTIGE_TYPES['PRESTIGE4']['NAME']
        user.profile.credit_limit = PRESTIGE_TYPES['PRESTIGE4']['LIMIT']
        user.profile.save()


def add_points(user, points):
    user.profile.positive_points += points
    user.profile.save()
    

def remove_points(user,points):
    user.profile.negative_points += points
    user.profile.save()


def check_critique(critique,user):
    from howmuch.settings import POINTS_FOR_POSITIVE_CRITIQUE, POINTS_FOR_NEGATIVE_CRITIQUE

    if critique.critique == 'E':
        add_points(user,POINTS_FOR_POSITIVE_CRITIQUE)
    elif critique.critique == 'M':
        remove_points(user,POINTS_FOR_NEGATIVE_CRITIQUE)






    

