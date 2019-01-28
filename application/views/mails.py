
from django.urls import reverse_lazy


from post_office.models import EmailTemplate

from application.models import Space, DataCreditLog




from post_office import mail


	
def to_moderator(DataCreditLog,moderators):
   
	url = "http://localhost:8000/space/"+str(DataCreditLog.space_id)
	credit =str(DataCreditLog.credit)
	if moderators == None:
		mail.send(
			   ['ana@parthenontech.com'], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			   template= 'onchange_notification',
			   context={'url':url, 'credit':credit,'name':'Ana'},)
	else:
		for moderator  in moderators:
			name= moderator.user.first_name
			email=moderator.user.email
			mail.send(
			  [email], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			   template= 'onchange_notification',
			   context={'url':url, 'credit':credit,'name':name},)