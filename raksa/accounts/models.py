from django.db import models
from django.contrib.auth.models import User
#importing signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField


# @receiver(post_save,sender = User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         Profile.objects.create(user = instance)

def profile_image_path_location(instance,filename):
    #today date
    today_date = datetime.now().strftime('%Y-%m-%d')
    return 'profile/%s/%s/%s' % (instance.user.username,today_date,filename)

@receiver(post_save, sender=User)
def create_user_profile(sender,instance, **kwargs):
    #if a user already exist and has no profile create
    Profile.objects.get_or_create(user=instance)
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    job_title  = models.CharField(max_length=255,blank=True,null=True)
    skills = models.TextField(null=True,blank=True)
    education_level = models.TextField(null=True,blank=True)
    phone = PhoneNumberField(null = True,blank=True,unique=True)
    bio = models.TextField(null=True,blank=True)
    profile_picture = models.ImageField(upload_to = profile_image_path_location,blank = True,null = True)
    location = models.CharField(max_length=255,blank = True,null=True)
    date_of_birth = models.DateField(null=True,blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username   
    


    @property
    def profile_picture_url(self):
        try:
            image = self.profile_picture.url
        except:
            image ="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROeLviaV4cJN472_w_6e7g8s3PZIYHQR_56WqIXec4EPfhQSbmSIOmIVg&s"
        return image

    @property
    def full_name(self):
        name = self.user.get_full_name()
        if name:
            return name
        return self.user.get_username()   

    def date_joined(self):
        time_difference = timezone.now() - self.user.date_joined
        if time_difference <= timedelta(days = 2):
           return  timesince(self.user.date_joined) + 'ago'
        else:
            return self.user.date_joined.strftime('%d %b')  
    
    
         
               
