from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from application.models import  Space, DataCreditLog
from application.models.user import Moderator
from post_office import mail
from post_office.models import EmailTemplate
from django.contrib.auth import get_user_model; 
User = get_user_model(); 
class Command(BaseCommand):
  help = 'Creates the Superuser called admin and the Templates for creation and suggested changes  mails'
  def handle(self, *args, **options):
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

   def createSuperuser():
   
    try:
      Admin= User.objects.get(username='admin')
    except:
      Admin= None
    if Admin is None:
      User.objects.create_superuser(username='admin', password='173685', email='ana@parthenontech.com', is_staff=True, is_superuser=True)
      Admin= User.objects.get(username='admin')
      moderator = Moderator.objects.create(user=Admin)
    else :
      Admin.email= 'ana@parthenontech.com'
      Admin.is_staff=True
      Admin.save()
      try:
       moderator=  Moderator.objects.get(user=Admin)
      except:
       moderator = None
      if moderator is None:
        moderator = Moderator.objects.create(user=Admin)
    
   try:
    createTemplates()
   except:
    pass
   createSuperuser()
   

    
       