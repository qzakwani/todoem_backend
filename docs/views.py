from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
def docs(request, *args, **kwargs):
    return render(request, 'docs.html')

@api_view(['GET'])
def schema(request, *args, **kwargs):
    return Response({
  "openapi": "3.0.0",
  "info": {
    "title": "Sample API",
    "description": "This is a sample API for demonstrating OpenAPI 3.0.",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://api.example.com/v1"
    }
  ],
  "paths": {
    "/users": {
      "get": {
        "summary": "Get a list of users",
        "operationId": "getUsers",
        "responses": {
          "200": {
            "description": "A list of users",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    
                  }
                }
              }
            }
          }
        }
      }
    }
    }
    })