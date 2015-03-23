from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem

# this pre-populates the database prior to any user interaction.  
# any changes here won't be seen unless the database is rebuilt

# name of operational task, link to task, and link to exit survey
test_tasks =  [
{
	'name': 'Test-OT1',
	'ot_survey_url': 'https://www.surveymonkey.com/s/LR37HZG',
	'ot_exit_url': 'https://www.surveymonkey.com/s/VD8NQZT'
},
{
	'name': 'Test-OT2',
	'ot_survey_url': 'https://www.surveymonkey.com/s/LR37HZG',
	'ot_exit_url': 'https://www.surveymonkey.com/s/VD8NQZT'
}
]

class Command(BaseCommand):    
    help = 'our help string comes here'

    def _create_user(self):
        user = User(username='test@test.com', password=make_password('test'))
        user.email = user.username
        user.save()
        userprofile = UserProfile(user=user)
        userprofile.save()

    	# get random product and sequence of operational tasks
        product = Product.objects.filter(is_active=True).order_by('?')[0]
        dataset = product.dataset
        matched_tasks = dataset.optask_set.filter(is_active=True).order_by('?')

    	for index, task in enumerate(matched_tasks[0:matched_tasks.count()]):
            TaskListItem(userprofile=userprofile, 
                product=product,
                op_task=task, 
                index=index, 
                task_active=False, 
                exit_active=False).save()

    def _create_data(self):
		dataset = Dataset(name='Test-DS', version='v0.1')
		dataset.save()
		
		Product(dataset=dataset, 
            url='/static/testing/index.html', 
            instructions=settings.STATIC_URL + 'testing/instructions.html', 
            team='test-team', 
			name='test-product',
			version='v0.1').save()

		for task in test_tasks:
			newtask = OpTask(dataset=dataset,
				name=task['name'],
				survey_url=task['ot_survey_url'],
				exit_url=task['ot_exit_url']).save() 

    def handle(self, *args, **options):
        self._create_data()
        self._create_user()