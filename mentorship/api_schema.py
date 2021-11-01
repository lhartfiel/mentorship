import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from mentorusers.models import MentorshipUser, Mentee
from progress.models import Progress, Session


class AuthMutation(graphene.ObjectType):
	register = mutations.Register.Field()
	verify_account = mutations.VerifyAccount.Field()
	resend_activation_email = mutations.ResendActivationEmail.Field()
	send_password_reset_email = mutations.SendPasswordResetEmail.Field()
	password_reset = mutations.PasswordReset.Field()
	password_change = mutations.PasswordChange.Field()
	archive_account = mutations.ArchiveAccount.Field()
	delete_account = mutations.DeleteAccount.Field()
	update_account = mutations.UpdateAccount.Field()
	send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
	verify_secondary_email = mutations.VerifySecondaryEmail.Field()
	swap_emails = mutations.SwapEmails.Field()

	# django-graphql-jwt inheritances
	token_auth = mutations.ObtainJSONWebToken.Field()
	verify_token = mutations.VerifyToken.Field()
	refresh_token = mutations.RefreshToken.Field()
	revoke_token = mutations.RevokeToken.Field()

	# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImxoYXJ0ZmllbCIsImV4cCI6MTYzNTczNTE2MCwib3JpZ0lhdCI6MTYzNTczNDg2MH0.ketpFlYJJC2yiyI2bmK1FciSl8 - V0SH86suhkKL0Z1I

class Mutation(AuthMutation, graphene.ObjectType):
	pass

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


class Query(UserQuery, MeQuery, graphene.ObjectType):
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


schema = graphene.Schema(query=Query, mutation=Mutation)