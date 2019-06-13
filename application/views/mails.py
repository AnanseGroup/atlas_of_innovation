
from post_office.models import EmailTemplate
from post_office import mail
from django.contrib.auth.models import User
from django.conf import settings as djangoSettings
'''Create the email templates on db'''

#mail sender, on space create

def on_create(DataCreditLog,moderators):
	url = djangoSettings.URL+"/analyze/provisional_spaces/"
	credit=str(DataCreditLog.credit)
	print('send to')
	print(moderators)
	if not moderators:
		mail.send(['ana@parthenontech.com','shewaw1@gmail.com'],'noreply@atlasofinnovation.com', priority='now',template='oncreate_notification',context={'url':url,'name':'Admin',})

	else:
		for moderator in moderators:
			if moderator.user.first_name:
			 name = moderator.user.first_name
			else:
			 name ="Moderator"	
			email= moderator.user.email
			
			email = moderator.user.email
			print(email)
			mail.send([email],'noreply@atlasofinnovation.com',template='oncreate_notification',context={'url':url,'name':name,},)

#mail sender, on space change
def on_change(DataCreditLog,moderators):  
	url = djangoSettings.URL+"/space/"+str(DataCreditLog.space_id)
	credit=str(DataCreditLog.credit)
	print('send to')
	print(moderators)
	if not moderators :
		mail.send(['ana@parthenontech.com','shewaw1@gmail.com'],'noreply@atlasofinnovation.com',template='onchange_notification',context={'url':url,'name':'Admin',})

	else:
	   for moderator  in moderators:
	   	    if moderator.user.first_name:
	   	    	name = moderator.user.first_name
	   	    else:
	   	    	name ="Moderator"
	   	    email= moderator.user.email
	   	    mail.send(
			  [email], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			    priority='now',template= 'onchange_notification',
			   context={'url':url,'name':name,'credit':credit,})




