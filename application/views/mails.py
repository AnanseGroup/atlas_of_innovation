
from django.urls import reverse_lazy


from post_office.models import EmailTemplate

from application.models import Space, DataCreditLog




from post_office import mail


	
def to_moderator(DataCreditLog):
   
	url = "http://localhost:8000/space/"+str(DataCreditLog.space_id)
	credit =str(DataCreditLog.credit)
	mail.send(
		   ['ana@parthenontech.com'], #List of email addresses also accepted  
			'noreply@atlasofinnovation.com',
		   template= 'onchange_notification',
		   context={'url':url, 'credit':credit,'name':'Ana'},)
		 