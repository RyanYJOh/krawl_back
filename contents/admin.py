from django.contrib import admin
from .models import Contents_Detail, WinnerContents_Detail, Likes_History, Likes_Master

# Register your models here.
class ContentsAdmin(admin.ModelAdmin):
    readonly_fields = ('id'),

admin.site.register(Contents_Detail, ContentsAdmin)
admin.site.register(WinnerContents_Detail, ContentsAdmin)
admin.site.register(Likes_History, ContentsAdmin)
admin.site.register(Likes_Master, ContentsAdmin)
