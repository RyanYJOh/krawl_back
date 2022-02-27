from operator import mod
from django.db import models
from django.contrib.auth.models import User
from votes.models import Competitions_Master, Points_Master

class Contents_Detail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content', null=False)
    competition_id = models.ForeignKey(Competitions_Master, on_delete=models.CASCADE, related_name='content', null=False)
    url = models.URLField(null=False)
    raw_date = models.DateField(auto_now_add=False)
    created_at = models.DateField(auto_now_add=True)
    date_check = models.BooleanField(default=False)
    opinion = models.TextField(blank=True)
    tag = models.CharField(max_length=200, blank=True)
    del_yn = models.BooleanField(default=False)

class WinnerContents_Detail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner_content', null=False)
    content_id = models.ForeignKey(Contents_Detail, on_delete=models.CASCADE, related_name='winner_content', null=False)
    competition_id = models.ForeignKey(Competitions_Master, on_delete=models.CASCADE, related_name='winner_content', null=False)
    point_id = models.ForeignKey(Points_Master, on_delete=models.CASCADE, related_name='winner_content', null=False)
    awarded_at = models.DateField(auto_now_add=False)

class Likes_History(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', null=False)
    content_id = models.ForeignKey(Contents_Detail, on_delete=models.CASCADE, related_name='likes', null=False)
    del_yn = models.BooleanField(default=False)
