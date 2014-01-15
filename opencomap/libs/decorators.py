from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from opencomap.libs.exceptions import MalformedBody

from django.contrib.auth.models import User
from opencomap.apps.backend.models.projects import Project
from opencomap.apps.backend.models.usergroup import UserGroup


def handle_http_errors(func):
	def wrapped(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except PermissionDenied, err:
			return HttpResponse(err, status=401)
		except User.DoesNotExist, err:
			return HttpResponse(err, status=404)
		except Project.DoesNotExist, err:
			return HttpResponse(err, status=404)
		except UserGroup.DoesNotExist, err:
			return HttpResponse(err, status=404)
	
	return wrapped

def handle_malformed(func):
	def wrapped(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except MalformedBody, err:
			return HttpResponse(err, status=400)
	
	return wrapped