from django.db import models
from django.contrib.auth.models import User

class Points_Master(models.Model):
    point_name = models.CharField(max_length=20, blank=False)
    get_point = models.IntegerField(null=False)

class Competitions_Master(models.Model):
    point_id = models.ForeignKey(Points_Master, on_delete=models.CASCADE, related_name='competitions', null=False)
    starts_at = models.DateField(auto_now_add=False)
    ends_at = models.DateField(auto_now_add=False)


