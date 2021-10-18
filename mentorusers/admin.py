from django.contrib import admin

# Register your models here.
from mentorusers.models import MentorshipUser, Mentee, Mentor


class MenteeInline(admin.TabularInline):
  model = Mentee
  fields = ['mentor',]

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    all_mentees = MentorshipUser.objects.filter(is_mentee=True)
    current_mentor = Mentor.objects.get(id=request.user.id)
    mentors_with_mentees = Mentor.objects.filter(mentors__mentee__in=all_mentees)

    # TODO - add filter by session
      # .exclude(mentor__mentee__session=self.session)
    if db_field.name == 'mentor':
      assigned_mentors = MentorshipUser.objects.filter(mentor__in=mentors_with_mentees).exclude(mentor=current_mentor)
      kwargs['queryset'] = Mentor.objects.exclude(mentor__in=assigned_mentors)
    return super(MenteeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class MentorshipUserAdmin(admin.ModelAdmin):

  inlines = [MenteeInline,]

  def change_view(self, request, object_id, form_url='', extra_context=None):
    try:
      obj = self.model.objects.get(pk=object_id)
      if obj and obj.is_mentee:
        self.inlines = [MenteeInline, ]
    except self.model.DoesNotExist:
      pass
    return super(MentorshipUserAdmin, self).change_view(request, object_id, form_url, extra_context)



admin.site.register(MentorshipUser, MentorshipUserAdmin)
# admin.site.register(Mentee)
# admin.site.register(Mentor)