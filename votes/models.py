from django.db import models
from django.contrib.auth.models import User

class Points_Master(models.Model):
    point_name = models.CharField(max_length=20, blank=False)
    get_point = models.IntegerField(null=False)

    def __str__(self):
        return self.point_name + ' : ' + str(self.get_point)

class Competitions_Master(models.Model):
    point_id = models.ForeignKey(Points_Master, on_delete=models.CASCADE, related_name='competitions', null=False)
    starts_at = models.DateField(auto_now_add=False)
    ends_at = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.point_id.point_name + ' : ' + str(self.starts_at) + '~' + str(self.ends_at)


