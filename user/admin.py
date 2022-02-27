from django.contrib import admin
from .models import UserPoint_History, UserPoint_Master, UserProfile_Master

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    readonly_fields = ('id'),

admin.site.register(UserProfile_Master, UsersAdmin)
admin.site.register(UserPoint_History, UsersAdmin)
admin.site.register(UserPoint_Master, UsersAdmin)