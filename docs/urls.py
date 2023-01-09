from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.docs),
    path("v2/", v.docs_v2),
    path("generated/", v.generated_schema, name='generated-schema'),
    path("schema/", v.schema, name='schema'),
    
    path("edit/", v.edit_docs, name="edit-docs")
    
    
]
