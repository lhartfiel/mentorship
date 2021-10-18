import graphene
from graphene_django import DjangoObjectType, DjangoListField

from mentorusers.models import MentorshipUser, Mentee
from progress.models import Progress, Session


class ProgressType(DjangoObjectType):
	class Meta:
		model = Progress
		fields = '__all__'

class MentorshipUserType(DjangoObjectType):
	class Meta:
		model = MentorshipUser
		fields = '__all__'


class MenteeType(DjangoObjectType):
	class Meta:
		model = Mentee
		fields = '__all__'

class SessionType(DjangoObjectType):
	class Meta:
		model = Session
		fields = '__all__'


class Query(graphene.ObjectType):
	all_progress = graphene.List(ProgressType)
	all_users = graphene.List(MentorshipUserType)
	all_sessions = graphene.List(SessionType)
	all_mentees_by_session = graphene.List(MenteeType, session=graphene.ID())
	all_mentors = graphene.List(MentorshipUserType)
	all_mentees = graphene.List(MentorshipUserType)

	def resolve_all_progress(root, info):
		return Progress.objects.all()

	def resolve_all_users(root, info):
		return MentorshipUser.objects.all()

	def resolve_all_mentors(root, info):
		return MentorshipUser.objects.filter(is_mentor=True)

	def resolve_all_mentees(root, info):
		return MentorshipUser.objects.filter(is_mentee=True)

	def resolve_all_sessions(root, info):
		return Session.objects.all()

	def resolve_all_mentees_by_session(root, info, session):
		try:
			session = session
			return Mentee.objects.filter(session__id=session)
		except Mentee.DoesNotExist:
			return



class ProgressInput(graphene.InputObjectType):
	pass


schema = graphene.Schema(query=Query)