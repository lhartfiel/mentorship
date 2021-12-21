import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType, DjangoListField
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from mentorusers.models import MentorshipUser, Mentee
from progress.models import Progress, Session, Accomplishment, Challenge


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


class MentorshipUserType(DjangoObjectType):
	class Meta:
		model = MentorshipUser
		fields = '__all__'

class MenteeType(DjangoObjectType):
	class Meta:
		model = Mentee
		fields = '__all__'

class ProgressType(DjangoObjectType):
	class Meta:
		model = Progress
		fields = '__all__'

class AccomplishmentType(DjangoObjectType):
	class Meta:
		model = Accomplishment
		fields = '__all__'

class ChallengeType(DjangoObjectType):
	class Meta:
		model = Challenge
		fields = '__all__'

class SessionType(DjangoObjectType):
	class Meta:
		model = Session
		fields = '__all__'

class MentorshipUserInput(graphene.InputObjectType):
	bio = graphene.String(help_text="Describe yourself -- hobbies, interests, coding career, etc.")
	first_name = graphene.String(max_length=255, blank=False)
	is_mentee = graphene.Boolean(default=False)
	is_mentor = graphene.Boolean(default=False)
	last_name = graphene.String(max_length=255, blank=True)
	photo = graphene.String(upload_to='user_photos')


class SessionInput(graphene.InputObjectType):
	date_session_start = graphene.DateTime(required=False)
	date_session_end = graphene.DateTime(required=False)
	name = graphene.String(required=False)
	id = graphene.Int()

class ProgressInput(graphene.InputObjectType):
	comments = graphene.String(required=False)
	date_start = graphene.DateTime(required=True)
	date_end = graphene.DateTime(required=True)
	# session = graphene.Field(SessionInput)
	summary = graphene.String(required=False)
	# user = MentorshipUserType

class ChallengeInput(graphene.InputObjectType):
	challenge = graphene.String(required=False)
	progress = graphene.Field(ProgressInput)

class AccomplishmentInput(graphene.InputObjectType):
	accomplishment = graphene.String(required=False)
	progress = graphene.Field(ProgressInput)

class CreateProgressInput(graphene.Mutation):
	class Arguments:
		progress = ProgressInput(required=True)
		challenge = ChallengeInput(required=False)
		accomplishments = graphene.List(AccomplishmentInput)
		session = SessionInput(required=False)
		username = graphene.String()

	# Output Fields
	ok = graphene.Boolean()
	progress = graphene.Field(ProgressType)
	accomplishment = graphene.Field(AccomplishmentType)
	challenge = graphene.Field(ChallengeType)
	session = graphene.Field(SessionType)

	@staticmethod
	def mutate(root, info, progress, challenge, accomplishments, session, username):
		ok=True
		user = MentorshipUser.objects.get(username__iexact=username)
		progress = Progress.objects.create(comments=progress.comments, summary=progress.summary, session_id=session.id, user_id=user.id, date_start=progress.date_start, date_end=progress.date_end)
		progress.save()
		for accomplishment in accomplishments:
			accomplishment = Accomplishment.objects.create(accomplishment=accomplishment.accomplishment, progress_id=progress.id)
			accomplishment.save()
		# accomplishment = Accomplishment.objects.create(accomplishment=accomplishment.accomplishment, progress_id=progress.id)
		challenge = Challenge.objects.create(challenge=challenge.challenge, progress_id=progress.id)
		challenge.save()
		return CreateProgressInput(progress=progress, challenge=challenge, accomplishment=accomplishments, ok=ok)

class Mutation(AuthMutation, graphene.ObjectType):
	create_progress_input = CreateProgressInput.Field()
	# mentorship_user = MentorshipUserType.Field()
	class Meta:
		model = MentorshipUser
		fields = '__all__'

class Query(UserQuery, MeQuery, graphene.ObjectType):
	all_progress = graphene.List(ProgressType, username=graphene.String(), session_id=graphene.ID())
	all_users = graphene.List(MentorshipUserType)
	all_sessions = graphene.List(SessionType)
	all_mentees_by_session = graphene.List(MenteeType, session=graphene.ID())
	all_mentors = graphene.List(MentorshipUserType)
	all_mentees = graphene.List(MentorshipUserType)
	user_access = graphene.Field(MentorshipUserType)

	def resolve_user_access(root, info):
		user = info.context.user
		if user.is_anonymous:
			raise Exception('Authentication Failure: Your must be signed in')
		if user.is_mentor or user.is_mentee:
			return get_user_model().objects.get(id=user.id)
		return MentorshipUser.objects.all()

	def resolve_all_progress(root, info, username, session_id):
		return Progress.objects.filter(user__username__iexact=username).filter(session_id=session_id)

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


schema = graphene.Schema(query=Query, mutation=Mutation)