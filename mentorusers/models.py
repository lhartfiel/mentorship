from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class MentorshipUser(AbstractUser):
	bio = models.TextField(help_text="Describe yourself -- hobbies, interests, coding career, etc.")
	first_name = models.CharField(max_length=255, blank=False)
	is_mentee = models.BooleanField(default=False)
	is_mentor = models.BooleanField(default=False)
	last_name = models.CharField(max_length=255, blank=True)
	photo = models.ImageField(upload_to='user_photos')

	USERNAME_FIELD = "username"  # e.g: "username", "email"
	EMAIL_FIELD = "email"  # e.g: "email", "primary_email"

	def __str__(self):
		return self.username


class Mentee(models.Model):
	mentee = models.OneToOneField(MentorshipUser, null=True, related_name='mentee', on_delete=models.CASCADE)
	mentor = models.ForeignKey("mentorusers.Mentor", null=True, on_delete=models.CASCADE, related_name='mentors')
	session = models.ForeignKey("progress.Session", default=1, related_name="mentee_session", on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.mentee.first_name}'


class Mentor(models.Model):
	mentor = models.ForeignKey(MentorshipUser, null=True, related_name='mentor', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.mentor.first_name}'


# Create a mentee when a new user is created and is_mentee is checked
def create_mentee(sender, **kwargs):
	instance = kwargs['instance']
	try:
		mentee = Mentee.objects.get(mentee__id=instance.id)
		if mentee:
			return
	except ObjectDoesNotExist:
		if instance.is_mentee:
			Mentee.objects.create(mentee=instance)


# Create a mentor when a new user is created and is_mentor is checked
def create_mentor(sender, **kwargs):
	instance = kwargs['instance']
	try:
		mentor = Mentor.objects.get(mentor__id=instance.id)
		if mentor:
			return
	except ObjectDoesNotExist:
		if instance.is_mentor:
			Mentor.objects.create(mentor=instance)
		else:
			return

post_save.connect(create_mentee, sender=MentorshipUser)
post_save.connect(create_mentor, sender=MentorshipUser)