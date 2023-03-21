from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Profile

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group =Group.objects.get(name='customer')
        instance.groups.add(group)

        Profile.objects.create(
				user=instance,
                name=instance.username,
			)
        print('Profile was created!!')

post_save.connect(customer_profile, sender=User)    



def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()
        print('Profile updated!!!')

post_save.connect(update_profile, sender=User)        