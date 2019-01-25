
from django.urls import reverse_lazy


from post_office.models import EmailTemplate

from application.models import Space, DataCreditLog




from post_office import mail


	
def to_moderator(DataCreditLog):
EmailTemplate.objects.create(
	    name='onchange_notification',
	    subject='Space Changes',
	    content='Hi {{ name }},',
	    html_content=' some changes had made in spacemade by <strong>{{ credit }}</strong> <br/>Check details<a href={{url}}>HERE</a>',
		)
url = "http://localhost:8000/space/"+str(DataCreditLog.space_id)
credit =str(DataCreditLog.credit)
mail.send(
	   ['orlandosalvadorcamarillomoreno@gmail.com'], #List of email addresses also accepted 'noreply@atlasofinnovation.com',
	   template= 'onchange_notification',
	   context={'url':url, 'credit':credit},)
	  # some changes was made in a space<br/> by <strong>{{ credit }}</strong><br/> if you want see the new space information click <a href="{{url}}">HERE</a>',
	  # )