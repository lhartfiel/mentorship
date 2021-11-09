from time import strftime

from django.db import models
from djrichtextfield.models import RichTextField


# Create your models here.
from mentorusers.models import MentorshipUser

class Progress(models.Model):
	comments = models.TextField(blank=True)
	date_start = models.DateTimeField(null=True, help_text="Start date should always be a Monday")
	date_end = models.DateTimeField(null=True, help_text="End date should always be a Friday")
	summary = RichTextField(blank=False, help_text="Provide a quote, an image, general thoughts to describe the week.")
	session = models.ForeignKey("progress.Session", related_name="progress_session", on_delete=models.CASCADE)
	user = models.ForeignKey(MentorshipUser, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.summary

class Accomplishment(models.Model):
	accomplishment = models.CharField(max_length=400, help_text="Concisely describe you accomplishment.")
	progress = models.ForeignKey('progress.Progress', null=True, related_name="accomplishment", on_delete=models.CASCADE)

	def __str__(self):
		return self.accomplishment


class Challenge(models.Model):
	challenge = models.CharField(max_length=400, help_text="Concisely describe your challenge.")
	progress = models.ForeignKey(Progress, null=True, related_name="challenge", on_delete=models.CASCADE)

	def __str__(self):
		return self.challenge


class Session(models.Model):
	date_session_start = models.DateTimeField()
	date_session_end = models.DateTimeField()
	name = models.CharField(max_length=255, help_text="Name for this session, such as Fall 2021")

	def __str__(self):
		return self.name