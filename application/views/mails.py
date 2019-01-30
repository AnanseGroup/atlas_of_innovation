
from post_office.models import EmailTemplate
from post_office import mail
from django.contrib.auth.models import User


	
def on_change(DataCreditLog,moderators):
   
	url = "http://localhost:8000/space/"+str(DataCreditLog.space_id)
	user=User.username
	print(moderators)
	if not moderators :
		mail.send(
			   ['orlandosalvadorcamarillomoreno@gmail.com'],#'ana@parthenontech.com'], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			   template= 'onchange_notification',
			   context={'url':url,'name':'Ana'},)
	else:
		for moderator  in moderators:

			name= moderator.user.first_name
			email=moderator.user.email
			print (email)
			mail.send(
			  [email], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			   template= 'onchange_notification',
			   context={'url':url,'name':name},)
 
