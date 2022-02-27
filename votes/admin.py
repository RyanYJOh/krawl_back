from django.contrib import admin
from .models import Points_Master, Competitions_Master

# Register your models here.
class VotesAdmin(admin.ModelAdmin):
    readonly_fields = ('id'),

admin.site.register(Points_Master, VotesAdmin)
admin.site.register(Competitions_Master, VotesAdmin)