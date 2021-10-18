from django.dispatch import receiver
from django.db.models.signals import post_save
import django.dispatch
from mentorusers.models import Mentee, MentorshipUser


create_mentee = django.dispatch.Signal()

def send_mentee(self, is_mentee):
    create_mentee.send(sender=self.__class__, is_mentee=self.is_mentee)

