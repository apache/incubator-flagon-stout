from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.conf.urls.static import static

from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment, Achievement

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

    def _create_admin_profile(self):
        staff_users = get_user_model().objects.filter(is_staff=True)
        admin = staff_users[0]
        print admin.email

        # check for existing admin profile before adding
        saved_userprofiles = UserProfile.objects.all()
        if [x for x in saved_userprofiles if x.user == admin] != []:
            print "admin user already exists."
            return;

        userprofile = UserProfile(user=admin)
        userprofile.save()
            
    def _create_user(self):
        # fix this later; need a logical method for experiment assignment
        saved_experiments = Experiment.objects.all()

        test_email = 'test@test.com'
        user = get_user_model()(email=test_email, password=make_password('test'))
        # check for existing test user before adding
        saved_userprofiles = UserProfile.objects.all()
        if [x for x in saved_userprofiles if x.user.email == test_email] != []:
            print "test user already exists."
            return

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
        test_exp_name = 'Test-exp'
        experiment = Experiment(name=test_exp_name, 
            task_count=2, 
            task_length=30, 
            has_achievements=True, 
            has_intake=True, 
            has_followup=True, 
            auto_tasking=True, 
            sequential_tasks=True, 
            consent=True)

        # check for existing test data before adding
        all_experiments = Experiment.objects.all();
        if [x for x in all_experiments if x.name == test_exp_name] != []:
            print "test experiment already exists."
            return

        experiment.save()
        
        # add a test dataset
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

        # add default achievements
        A1 = Achievement(name='tasksCompleteOne',
                         desc='Operational Tasks Complete')
        A2 = Achievement(name='tasksCompleteTwo',
                         desc='Operational Tasks Complete II')
        A3 = Achievement(name='freePlay',
                         desc='Free Play')

        A1.save()
        A2.save()
        A3.save()

    def handle(self, *args, **options):
        self._create_admin_profile()
        self._create_data()
        self._create_user()
