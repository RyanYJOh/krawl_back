from django.db import models
from django.contrib.auth.models import User
from votes.models import Points_Master

class Account(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile_Master(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', null=False)
    nickname = models.CharField(max_length=10, blank=False)
    profile_img = models.ImageField(null=True, upload_to='profile_imgs') # default='default_psa.jpg'

class UserPoint_History(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_point_history', null=False)
    point_id = models.ForeignKey(Points_Master, on_delete=models.CASCADE, related_name='user_point_history', null=False)
    received_at = models.DateField(auto_now_add=True)
    amount_point = models.IntegerField(null=False)

class UserPoint_Master(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_point', null=False)
    point_id = models.ForeignKey(Points_Master, on_delete=models.CASCADE, related_name='user_point', null=False)
    total_point = models.IntegerField(null=False)
    last_updated_at = models.DateField(auto_now_add=False)
