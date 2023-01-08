from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required 
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse

from .decorators import docs_puplic
from .schemas import generate_schema
from .dsettings import docs_settings


User = get_user_model()

@docs_puplic
def docs(request, *args, **kwargs):
  if docs_settings.USE_SAVED:
    url = "saved-schema"
  else:
    url = "generated-schema"
  return render(request, "docs/docs.html", {"schema": url})

@docs_puplic
def docs_v2(request, *args, **kwargs):
  if docs_settings.USE_SAVED:
    url = "saved-schema"
  else:
    url = "generated-schema"
  return render(request, "docs/docs_v2.html", {"schema": url})


def generated_schema(req, *args, **kwargs):
  if docs_settings.PUBLIC or (req.user.is_staff and req.user.is_active):
    return JsonResponse(generate_schema(req))
  else :
    return JsonResponse({})
    

def saved_schema(req, *args, **kwargs):
  if docs_settings.PUBLIC or (req.user.is_staff and req.user.is_active):
    return JsonResponse(generate_schema(req))
  else :
    return JsonResponse({})

@staff_member_required
def edit_docs(request, *args, **kwargs):
  pass

@staff_member_required
def add_endpoint_props(request, *args, **kwargs):
  pass

@staff_member_required
def edit_endpoint_props(request, *args, **kwargs):
  pass