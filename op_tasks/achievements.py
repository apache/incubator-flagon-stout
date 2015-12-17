from django.core.exceptions import ObjectDoesNotExist
from op_tasks.models import TaskListItem, UserAchievement, Achievement


def checkAchievements(request):
    """
    This appears to be an aggregate function that runs the various
    checks for each type of achievement. It should be safe to call this
    as various transition points as the user navigates around the UI.
    """
    user = request.user
    userprofile = user.userprofile

    # Check all individual achievement logics
    tasksComplete(user)
    #genTaskAccuracy(user)
    #devTaskAccuracy(user)
    #genTaskAccuracy(user)
    #referralsOne(user)
    #referralsTwo(user)
    #referralsThree(user)
    #referralsFour(user)
    
    # Gather and return the list of achievement objects
    tasksCompleteOneAchievement = Achievement.objects.get(name='tasksCompleteOne')
    return UserAchievement.objects.filter(userprofile=userprofile, achievement=tasksCompleteOneAchievement).exists()


def tasksComplete(user):
    """
    This is tied to the logic responsible for activating all of the tasksCompleteXXX achievements
    for the incoming user
    """
    award = False
    userprofile = user.userprofile
    
    # See if user already has the achievement, if so, just move on
    tasksCompleteOneAchievement = Achievement.objects.get(name='tasksCompleteOne')
    try:
        userAchievement = UserAchievement.objects.get(userprofile=userprofile, achievement=tasksCompleteOneAchievement)
    except ObjectDoesNotExist:
        # User does not have achievement yet... test to see if they should:
        try:
            if userprofile.tasklistitem_set.get(index=0).exit_complete:
                userAchievement = UserAchievement(userprofile=userprofile, achievement=tasksCompleteOneAchievement)
                userAchievement.save()
                award=True
        except TaskListItem.DoesNotExist:
            pass
            
    # TODO implement for tasksCompleteTwo
    tasksCompleteTwoAchievement = Achievement.objects.get(name='tasksCompleteTwo')
    try:
        userAchievement = UserAchievement.objects.get(userprofile=userprofile, achievement=tasksCompleteTwoAchievement)
    except ObjectDoesNotExist:
        # User does not have achievement yet... test to see if they should:
        try:
            if userprofile.tasklistitem_set.get(index=1).exit_complete:
                userAchievement = UserAchievement(userprofile=userprofile, achievement=tasksCompleteTwoAchievement)
                userAchievement.save()
                award=True
        except TaskListItem.DoesNotExist:
            pass
        
    return award


def hasTasksCompleteOneAchievement(user):
    userprofile = user.userprofile
    tasksCompleteOneAchievement = Achievement.objects.get(name='tasksCompleteOne')
    try:
        UserAchievement.objects.get(userprofile=userprofile, achievement=tasksCompleteOneAchievement)
        return True
    except ObjectDoesNotExist:
        return False

def hasTasksCompleteTwoAchievement(user):
    userprofile = user.userprofile
    tasksCompleteTwoAchievement = Achievement.objects.get(name='tasksCompleteTwo')
    try:
        UserAchievement.objects.get(userprofile=userprofile, achievement=tasksCompleteTwoAchievement)
        return True
    except ObjectDoesNotExist:
        return False

def genTaskAccuracy(user):
    award = False
    userprofile = user.userprofile
    genAccuracyAchivement = Achievement.objects.get(name='genTaskAccuracy')

    try:
        userAchievement = UserAchievement.objects.get(userprofile=userprofile, achievement=genAccuracyAchivement)
    except ObjectDoesNotExist:
        if userprofile.bestDevAccuracy > 89:
            userAchievement = UserAchievement(userprofile=userprofile, achievement=genAccuracyAchivement)
            userAchievement.save()
            award=True
    return award


def devTaskAccuracy(user):
    award = False
    userprofile = user.userprofile
    devAccuracyAchivement = Achievement.objects.get(name='devTaskAccuracy')

    try:
        userAchievement = UserAchievement.objects.get(userprofile=userprofile, achievement=devAccuracyAchivement)
    except ObjectDoesNotExist:
        if userprofile.bestDevAccuracy > 89:
            userAchievement = UserAchievement(userprofile=userprofile, achievement=devAccuracyAchivement)
            userAchievement.save()
            award=True
    return award


def referralsOne(user):
    """
    checks referrals in userprofile to see if a certain level is met
    :param user: the user object to check
    :return: boolean, true if condition met, false otherwise
    """
    return referralsCheck(user, 3, 'referralsOne')


def referralsTwo(user):
    """
    checks referrals in userprofile to see if level two is met
    :param user: the user object to check
    :return: award - boolean, true if condition met, false otherwise
    """
    return referralsCheck(user, 6, 'referralsTwo')


def referralsThree(user):
    """

    :param user:
    :return:
    """
    return referralsCheck(user, 9, 'referralsThree')


def referralsFour(user):
    """

    :param user:
    :return:
    """
    return referralsCheck(user, 12, 'referralsFour')


def referralsCheck(user, count, achievementName):
    """
    general method to check different levels of referrals
    :param user: the user object to check
    :param count: the level to check
    :param achievementName: the name of the achievement
    :return: boolean - true if level met, false otherwise
    """
    award = False
    userprofile = user.userprofile
    referralsAchievement = Achievement.objects.get(name=achievementName)

    # first check if user already has achievement
    try:
        userAchievement = UserAchievement.objects.get(userprofile=userprofile, achievement=referralsAchievement)
    except ObjectDoesNotExist:
        if userprofile.referrals >= count :
            userAchievement = UserAchievement(userprofile=userprofile, achievement=referralsAchievement)
            userAchievement.save()
            award = True
    return award


def awardFreePlayAchievement(user):
    """
    Awards the Free Play achievement to the indicated user
    IFF they don't already have it.
    """
    userprofile = user.userprofile
    freePlayAchievement = Achievement.objects.get(name='freePlay')
    
    try:
        UserAchievement.objects.get(userprofile=userprofile, achievement=freePlayAchievement)
    except ObjectDoesNotExist:
        userAchievement = UserAchievement(userprofile=userprofile, achievement=freePlayAchievement)
        userAchievement.save()
        
def hasFreePlayAchievement(user):
    userprofile = user.userprofile
    freePlayAchievement = Achievement.objects.get(name='freePlay')
    try:
        UserAchievement.objects.get(userprofile=userprofile, achievement=freePlayAchievement)
        return True
    except ObjectDoesNotExist:
        return False