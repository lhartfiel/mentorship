from django.contrib import admin

# Register your models here.
from progress.models import Session, Progress, Accomplishment, Challenge


class AccomplishmentInline(admin.TabularInline):
    model = Accomplishment

class ChallengeInline(admin.TabularInline):
    model = Challenge

class ProgressAdmin(admin.ModelAdmin):
    inlines = [
        AccomplishmentInline,
	      ChallengeInline
    ]

admin.site.register(Session)
admin.site.register(Progress, ProgressAdmin)