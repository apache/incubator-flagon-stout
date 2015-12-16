from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment

def appendAllTasks(user):
    """
    This function is responsible for adding all available tasks
    to the indicated user. It respects whether tasks and products
    are active (available) and only associates the correct
    tasking with the product that is applicable.
    
    This is used in at least two places: when the user activiates
    the Free Play achievement, and when a new user is registered
    under All Products.
    """
    userprofile = user.userprofile
    index = userprofile.tasklistitem_set.all().count()
    datasets = Dataset.objects.all()        
    for dataset in datasets:
        products = dataset.product_set.all()
        products = products.filter(is_active=True)
        for product in products:
            tasks = dataset.optask_set.all()
            tasks = tasks.filter(is_active=True)
            for task in tasks:
                newtasklistitem = TaskListItem()
                newtasklistitem.userprofile = userprofile
                newtasklistitem.op_task = task
                newtasklistitem.product = product
                newtasklistitem.index = index
                index = index + 1
                newtasklistitem.task_active = True
                newtasklistitem.save()