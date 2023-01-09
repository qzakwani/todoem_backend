import json

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required 
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse

from .schemas import generate_schema, generate_eidt_schema
from .dsettings import docs_settings as s, project
from .models import DocsSchema, DocsSettings

User = get_user_model()

def docs(request, *args, **kwargs):
  if s.PUBLIC or DocsSettings.objects.filter(public=True).exists():
    return render(request, "docs/docs.html", {"schema": "generated-schema" if s.USE_GENERATED else "schema",
                                              "proj_name": project})
  elif request.user.is_staff and request.user.is_active:
    return render(request, "docs/docs.html", {"schema": "generated-schema" if s.USE_GENERATED else "schema", 
                                              "proj_name": project})
  else:
    from django.contrib.auth import REDIRECT_FIELD_NAME
    from django.shortcuts import resolve_url
    from urllib.parse import urlparse
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(s.LOGIN_URL)
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if (not login_scheme or login_scheme == current_scheme) and (
        not login_netloc or login_netloc == current_netloc
    ):
        path = request.get_full_path()
    from django.contrib.auth.views import redirect_to_login

    return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)
    


def docs_v2(request, *args, **kwargs):
  if s.PUBLIC or DocsSettings.objects.filter(public=True).exists():
    return render(request, "docs/docs_v2.html", {"schema": "generated-schema" if s.USE_GENERATED else "schema", "proj_name": project})
  elif request.user.is_staff and request.user.is_active:
    return render(request, "docs/docs_v2.html", {"schema": "generated-schema" if s.USE_GENERATED else "schema", "proj_name": project})
  else:
    from django.contrib.auth import REDIRECT_FIELD_NAME
    from django.shortcuts import resolve_url
    from urllib.parse import urlparse
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(s.LOGIN_URL)
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if (not login_scheme or login_scheme == current_scheme) and (
        not login_netloc or login_netloc == current_netloc
    ):
        path = request.get_full_path()
    from django.contrib.auth.views import redirect_to_login

    return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)


def generated_schema(request, *args, **kwargs):
  if s.PUBLIC or DocsSettings.objects.filter(public=True).exists():
    return JsonResponse(generate_schema(request))
  elif request.user.is_staff and request.user.is_active:
    return JsonResponse(generate_schema(request))
  else:
    return JsonResponse(s.UNAUTHORIZED_RESPONSE)

    

def schema(request, *args, **kwargs):
  try:
    _schema = DocsSchema.objects.get(default=True)
  except DocsSchema.DoesNotExist:
    _schema = s.EMPTY_RESPONSE
  if s.PUBLIC or DocsSettings.objects.filter(public=True).exists():
    return JsonResponse(_schema)
  elif request.user.is_staff and request.user.is_active:
    return JsonResponse(_schema)
  else:
    return JsonResponse(s.UNAUTHORIZED_RESPONSE)


# @staff_member_required
def edit_docs(request, *args, **kwargs):
  _schema = generate_eidt_schema(request)
  return render(request, "docs/edit.html", {"gen_schema": json.dumps(_schema), "proj_name": project})

@staff_member_required
def add_endpoint_props(request, *args, **kwargs):
  pass

@staff_member_required
def edit_endpoint_props(request, *args, **kwargs):
  pass