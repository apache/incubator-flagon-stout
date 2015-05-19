from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment

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
        # fix this later; need a logical method for experiment assignment
        saved_experiments = Experiment.objects.all()

        user = User(username='test@test.com', password=make_password('test'))
        user.email = user.username
        user.save()

        userprofile = UserProfile(user=user)
        userprofile.experiment = saved_experiments[0]
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
		experiment = Experiment(name='Test-exp', 
            task_count=2,
            task_length=30,
            has_achievements=True,
            has_intake=True,
            has_followup=True,
            auto_tasking=True)

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