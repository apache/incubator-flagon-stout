from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from op_tasks.models import *

# this pre-populates the database prior to any user interaction.  
# any changes here likely won't be seen unless the database is rebuilt

# name of operational task, link to task, and link to exit survey
kiva_ots =  [
('Kiva-OT1','https://www.surveymonkey.com/jsEmbed.aspx?sm=sxPflNw3jozCzZypcqWRQw_3d_3d', 
	'https://www.research.net/jsEmbed.aspx?sm=tYJM5iagWbyhqTn4_2fiY9Vg_3d_3d'),
('Kiva-OT2','https://www.surveymonkey.com/jsEmbed.aspx?sm=IpK_2f4QEuQ4gHlzXW23Jwmw_3d_3d', 
	'https://www.research.net/jsEmbed.aspx?sm=ENjFjhorB6q_2fS_2f7XTBG8gA_3d_3d'),
('Kiva-OT3','https://www.surveymonkey.com/jsEmbed.aspx?sm=aYs37Ot_2fVlOBNcbfMH1yUg_3d_3d', 
	'https://www.research.net/jsEmbed.aspx?sm=ny3fOPYFSUODDGx5w8guYA_3d_3d')
]

class Command(BaseCommand):    
    help = 'our help string comes here'

    def _create_participants(self):
    	participant = Participant(email="test@test.com", password=make_password("test"))

    	product = Product.objects.filter(is_active=True).order_by('?')[0]
        dataset = product.dataset

        # get random sequence of operational tasks
        # operational_tasks = dataset.optask_set.filter(is_active=True).order_by('?')

        # assign it to the user
        setattr(participant, 'product', product)

    	participant.save()

    def _create_data(self):
		kiva = Dataset(name='Kiva', version='v0.1')
		kiva.save()
		# print kiva_ots[0][0]
		
		influent = Product(
			dataset=kiva, 
			url='xd-viz-ws3:8080/kiva/', 
			team='Oculus', 
			name='Influent',
			version='v0.1').save()

		for ot in kiva_ots:
			ot1 = OpTask(
				dataset=kiva,
				name=ot[0],
				survey_url=ot[1],
				exit_url=ot[2]).save() 

    def handle(self, *args, **options):
        self._create_data()
        self._create_participants()