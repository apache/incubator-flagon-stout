from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from op_tasks.models import *
from django.conf import settings
from django.conf.urls.static import static

# this pre-populates the database prior to any user interaction.  
# any changes here won't be seen unless the database is rebuilt

# name of operational task, link to task, and link to exit survey
test_ot =  [
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

    def _create_participants(self):
    	participant = Participant(email="test@test.com", password=make_password("test"))

    	product = Product.objects.filter(is_active=True).order_by('?')[0]
        dataset = product.dataset

        # get random sequence of operational tasks
        operational_tasks = dataset.optask_set.filter(is_active=True).order_by('?')

        # assign it to the user
        setattr(participant, 'product', product)
    	participant.save()

    	for ot_index, ot in enumerate(operational_tasks[0:3]):
            if ot_index==0:
                ot_active=True
            else:
                ot_active=False
            exit_active=False
            Sequence(
            	user=participant, 
            	op_task=ot, 
            	index=ot_index, 
            	ot_active=ot_active, 
            	exit_active=exit_active
            	).save()

    def _create_data(self):
		test = Dataset(name='Test-DS', version='v0.1')
		test.save()
		
		Product(
			dataset=test, 
			url='/static/testing/index.html',
            instructions=settings.STATIC_URL + 'testing/instructions.html',
			team='test-team', 
			name='test-product',
			version='v0.1'
			).save()

		for ot in test_ot:
			ot1 = OpTask(
				dataset=test,
				name=ot['name'],
				survey_url=ot['ot_survey_url'],
				exit_url=ot['ot_exit_url']
				).save() 

    def handle(self, *args, **options):
        self._create_data()
        self._create_participants()