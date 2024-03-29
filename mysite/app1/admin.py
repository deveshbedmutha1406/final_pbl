"""Admin View Configuration"""
from django.contrib import admin
from .models import Applications, WorkType, Work, Images, ManyToManyRelation

@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    """Admin View For Application Table"""
    list_display = ["id", "user", "contact_no", "type"]


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    """Admin View For WorkType Table"""
    list_display = ["id", "TypeOfWork"]


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    """Admin View For Work Table"""
    list_display = ["id", "work_id", "Hours", "Wages", "approved", "city"]


admin.site.register(Images)


@admin.register(ManyToManyRelation)
class ManyToManyRelationAdmin(admin.ModelAdmin):
    """Admin View For Relation Table"""
    list_display = ["id", "userid", "workid"]
