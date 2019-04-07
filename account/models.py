from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (('male', 'M'), ('female', 'F'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(verbose_name='your image', upload_to='account/profile', blank=True)
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=50)

    def __str__(self):
        return 'profile for user {}'.format(self.user)

class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

User.add_to_class('following', models.ManyToManyField('self', related_name='followers', symmetrical=False, through=Contact))

