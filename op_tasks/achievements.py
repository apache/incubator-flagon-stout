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
    if request.method == 'POST':
        user = request.user
        userprofile = user.userprofile
    return True
