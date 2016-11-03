"""Views for social interactions."""

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.contrib import messages

from braces.views import LoginRequiredMixin
from allauth.socialaccount.models import SocialAccount

from geokey.core.decorators import handle_exceptions_for_admin
from geokey.projects.models import Project
from geokey.projects.views import ProjectContext

from .models import SocialInteraction


class SocialInteractionList(LoginRequiredMixin, ProjectContext, TemplateView):
    """Display the list of social interactions in the project."""

    template_name = 'socialinteractions/socialinteraction_list.html'


class SocialInteractionCreate(LoginRequiredMixin, ProjectContext,
                              TemplateView):
    """Provide the form to create a new social interaction."""

    template_name = 'socialinteractions/socialinteraction_create.html'

    def get_context_data(self, project_id, *args, **kwargs):
        """
        Return the context to render the view.

        Add Twitter and Facebook social accounts of a user to the context.

        Parameters
        ----------
        project_id : int
            Identifies the project in the database.

        Returns
        -------
        dict
            Context.
        """
        context = super(SocialInteractionCreate, self).get_context_data(
            project_id,
            *args,
            **kwargs
        )

        context['socialaccounts'] = SocialAccount.objects.filter(
            user=self.request.user,
            provider__in=['twitter', 'facebook']
        )

        return context

    def post(self, request, project_id):
        """
        Create the social interaction based on the data entered by the user.

        Parameters
        ----------
        request : django.http.HttpRequest
            Object representing the request.
        project_id : int
            Identifies the project in the database.

        Returns
        -------
        django.http.HttpResponseRedirect
            Redirects to social interaction settings page if social interaction
            is created, social interaction create page if project is locked or
            social account is not found.
        django.http.HttpResponse
            Rendered template, if project does not exist.
        """
        data = request.POST
        context = self.get_context_data(project_id)
        project = context.get('project')

        if project:
            cannot_create = 'New social interactions cannot be created.'

            if project.islocked:
                messages.error(
                    self.request,
                    'The project is locked. %s' % cannot_create
                )
                return redirect(
                    'admin:socialinteraction_create',
                    project_id=project_id
                )

            try:
                socialaccount = SocialAccount.objects.get(
                    pk=data.get('socialaccount'))
            except SocialAccount.DoesNotExist:
                messages.error(
                    self.request,
                    'The social account is not found. %s' % cannot_create
                )
                return redirect(
                    'admin:socialinteraction_create',
                    project_id=project_id
                )

            socialinteraction = SocialInteraction.objects.create(
                name=strip_tags(data.get('name')),
                description=strip_tags(data.get('description')),
                creator=request.user,
                project=project,
                socialaccount=socialaccount
            )

            add_another_url = reverse(
                'admin:socialinteraction_create',
                kwargs={
                    'project_id': project_id
                }
            )

            messages.success(
                self.request,
                mark_safe('The social interaction has been created. '
                          '<a href="%s"> Add another social '
                          'interaction.</a>' % add_another_url)
            )

            return redirect(
                'admin:socialinteraction_settings',
                project_id=project_id,
                socialinteraction_id=socialinteraction.id
            )
        else:
            return self.render_to_response(context)


class SocialInteractionContext(object):
    """Provide the context to render templates."""

    @handle_exceptions_for_admin
    def get_context_data(self, project_id, socialinteraction_id,
                         *args, **kwargs):
        """
        Return the context to render the view.

        Add social interaction to the context.

        Parameters
        ----------
        project_id : int
            Identifies the project in the database.
        socialinteraction_id : int
            Identifies the social interaction in the database.

        Returns
        -------
        dict
            Context.
        """
        project = Project.objects.as_admin(self.request.user, project_id)

        try:
            socialinteraction = project.socialinteractions.get(
                pk=socialinteraction_id)
        except:
            messages.error(
                self.request, 'The social interaction is not found.'
            )
            return redirect(
                'socialinteractions/socialinteraction_settings.html',
                project_id=project_id,
                socialinteraction_id=socialinteraction_id,
            )

        return super(SocialInteractionContext, self).get_context_data(
            project=project,
            socialinteraction=socialinteraction,
        )


class SocialInteractionSettings(LoginRequiredMixin, SocialInteractionContext,
                                TemplateView):
    """Provide the form to update the social interaction settings."""

    template_name = 'socialinteractions/socialinteraction_settings.html'

    def post(self, request, project_id, socialinteraction_id):
        """
        Update the social interaction based on the data entered by the user.

        Parameter
        ---------
        request : django.http.HttpRequest
            Object representing the request.
        project_id : int
            Identifies the project in the database.
        socialinteraction_id : int
            Identifies the social interaction in the database.

        Returns
        -------
        django.http.HttpResponse
            Rendered template when social interactions updated.
        django.http.HttpResponse
            Rendered template, if project or social interaction does not exist.
        """
        data = request.POST
        context = self.get_context_data(project_id, socialinteraction_id)
        socialinteraction = context.get('socialinteraction')

        if socialinteraction:
            socialinteraction.name = strip_tags(data.get('name'))
            socialinteraction.description = strip_tags(data.get('description'))
            socialinteraction.save()

            messages.success(
                self.request,
                'The social interaction has been updated.'
            )

        return self.render_to_response(context)


class SocialInteractionDelete(LoginRequiredMixin, SocialInteractionContext,
                              TemplateView):
    """Delete the social interaction."""

    template_name = 'base.html'

    def get(self, request, project_id, socialinteraction_id):
        """
        Delete the social interaction.

        Parameter
        ---------
        request : django.http.HttpRequest
            Object representing the request.
        project_id : int
            Identifies the project in the database.
        socialinteraction_id : int
            Identifies the social interaction in the database.

        Returns
        -------
        django.http.HttpResponseRedirect
            Redirects to social interactions list if social interaction is
            deleted, social interaction settings if project is locked.
        django.http.HttpResponse
            Rendered template, if project or social interaction does not exist.
        """
        context = self.get_context_data(project_id, socialinteraction_id)
        socialinteraction = context.get('socialinteraction')

        if socialinteraction:
            if socialinteraction.project.islocked:
                messages.error(
                    self.request,
                    'The project is locked. Social interaction cannot be '
                    'deleted.'
                )
                return redirect(
                    'admin:socialinteraction_settings',
                    project_id=project_id,
                    socialinteraction_id=socialinteraction_id
                )

            socialinteraction.delete()
            messages.success(
                self.request,
                'The social interaction has been deleted.'
            )
            return redirect(
                'admin:socialinteraction_list',
                project_id=project_id
            )

        return self.render_to_response(context)