
from post_office.models import EmailTemplate
from post_office import mail
from django.contrib.auth.models import User
from django.conf import settings as djangoSettings

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper



#mail sender, on space change 

# def on_create(DataCreditLog,moderators):
# 	url = djangoSettings.URL+"space"+str(DataCreditLog.space_id)
# 	if not moderators:
# 		mail.send(['orlandosalvadorcamarillomoreno@gmail.com'],template='oncreate_notification',context={'url':url,'name':Ana,})
# 	else:
# 		for moderator in moderators:
# 			name=moderator.user.first_name
# 			email=moderator.user.email
# 			print(email)
# 			mail.send([email],template='oncreate_notification',context={'url':url,'name':name,},)


def on_change(DataCreditLog,moderators):  
	url = djangoSettings.URL+"space/"+str(DataCreditLog.space_id)
	user=User.username
	credit=str(DataCreditLog.credit)
	print(moderators)
	if not moderators :
		mail.send(
			   ['orlandosalvadorcamarillomoreno@gmail.com'],#'ana@parthenontech.com'], #List of email addresses also accepted  
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



@run_once
def createTemplates():
	EmailTemplate.objects.create(
	    name='onchange_notification',#
	    subject='Space changed, {{ name|capfirst }}',
	    
	    html_content='Hi <strong>{{ name }}</strong> some changes has made in a space by {{credit}}, click <a href={{url}}>here</a>to go to space'
	)

	EmailTemplate.objects.create(
	    name='oncreate_notification',#
	    subject='Space created, {{ name|capfirst }}',
	    
	    html_content='Hi <strong>{{ name }}</strong>  a new space was created , click <a href={{url}}>here</a>to go to space'
	)



createTemplates()