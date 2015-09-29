from op_tasks.models import UserProfile, \
    Product, Dataset, OpTask, TaskListItem, Experiment, \
    UserAchievement, Achievement

def checkAchievements(request):
    if tasksComplete(request):
        user = request.user
        userprofile = user.userprofile
        userachievement = UserAchievement()
        userachievement.userprofile = userprofile
        userachievement.achievement = Achievement.objects.get(name='tasksComplete')
        userachievement.save()


def tasksComplete(request):
    # if request.method == 'POST':
    #     user = request.user
    #     userprofile = user.userprofile
    return True


def genTaskAccuracy(request):
    return 10


def devTaskAccuracy(request):
    return 10


def referralsOne(request):
    return True


def referralsTwo(request):
    return True


def referralsThree(request):
    return True


def referralsFour(request):
    return True


