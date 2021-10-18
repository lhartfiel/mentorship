from django.views.generic import TemplateView

from mentorusers.models import Mentee


class HomepageView(TemplateView):
	template_name = "mentorship/home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		mentees = Mentee.objects.all()
		context["mentees"] = mentees
		return context
