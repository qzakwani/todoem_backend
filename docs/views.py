from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from .schemas import schema
from core.utils import get_base_url, get_urls

def docs(request, *args, **kwargs):
    return render(request, 'docs/docs.html')

@staff_member_required
def list_urls(request, *args, **kwargs):
  return render(request, "docs/urls.html", {"base": get_base_url(request), "paths": get_urls()})


@api_view(["GET"])
def hello(req, *args, **kwargs):
  return Response(schema(req).base_schema)