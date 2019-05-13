
from post_office.models import EmailTemplate
from post_office import mail
from django.contrib.auth.models import User
from django.conf import settings as djangoSettings
'''Create the email templates on db'''
def createTemplates():
	if not EmailTemplate.objects.filter(name='onchange_notification'):
		EmailTemplate.objects.create(
		    name='onchange_notification',#
		    subject='Space changed, {{ name|capfirst }}',
		    
		    html_content='Hi <strong>{{ name }}</strong> some changes has made in a space by {{credit}}, click <a href={{url}}>here</a>to go to space'
		)
	if not EmailTemplate.objects.filter(name='oncreate_notification'):
		EmailTemplate.objects.create(
		    name='oncreate_notification',#
		    subject='Space created, {{ name|capfirst }}',
		    
		    html_content='Hi <strong>{{ name }}</strong>  a new space was created , click <a href={{url}}>here</a> to go provisional spaces analizer'
		)
'''Error when post office is not installed '''
try:
	createTemplates()
except:
	pass
#mail sender, on space create

def on_create(DataCreditLog,moderators):
	url = djangoSettings.URL+"/analyze/provisional_spaces/"
	credit=str(DataCreditLog.credit)
	print('send to')
	print(moderators)
	if not moderators:
		mail.send(['ana@parthenontech.com','nirupama@saman-mali.com'],template='oncreate_notification',context={'url':url,'name':'Ana',})
	else:
		for moderator in moderators:
			name=moderator.user.first_name
			email=moderator.user.email
			print(email)
			mail.send([email],template='oncreate_notification',context={'url':url,'name':name,},)

#mail sender, on space change
def on_change(DataCreditLog,moderators):  
	url = djangoSettings.URL+"/space/"+str(DataCreditLog.space_id)
	credit=str(DataCreditLog.credit)
	print('send to')
	print(moderators)
	if not moderators :
		mail.send(
			   ['ana@parthenontech.com','nirupama@saman-mali.com'],#''], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			   template= 'onchange_notification',
			   context={'url':url,'name':'Ana','credit':credit,},)
	else:
		for moderator  in moderators:

			name= moderator.user.first_name
			email=moderator.user.email
			print (email)
			mail.send(
			  [email], #List of email addresses also accepted  
				'noreply@atlasofinnovation.com',
			   template= 'onchange_notification',
			   context={'url':url,'name':name,'credit':credit,})




