from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from . import models


class CommentAdmin(CompareVersionAdmin):
    list_display = ['id', 'parent_id', 'text', 'modified_at', 'created_at']

    class Meta:
        model = models.Comment


class ExportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at']

    class Meta:
        model = models.Export


admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Export, ExportAdmin)
