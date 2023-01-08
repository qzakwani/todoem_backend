import re

from django.apps.registry import apps
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .dsettings import docs_settings, settings
from .utils import APIEndpoint


class BaseSchemaGenerator:
    JWT_SECURITY = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    def __init__(self, request, base=None) -> None:
        self._base_schema = base
        self._endpoints = None
        self._req = request


    @property
    def base_schema(self) -> dict:
        if self._base_schema is None:
            self._base_schema = self.supply_base()
        return self._base_schema
        
    
    def supply_base(self):
        temp_schema = docs_settings.META
        temp_schema["components"] = {}
        if docs_settings.JWT_SECURITY["ADD"]:
            temp_schema['components']['securitySchemes'] = self.JWT_SECURITY
            if docs_settings.JWT_SECURITY["ALL"]:
                temp_schema["security"] = [{"Bearer": []}]
        
        if docs_settings.TAGS is not None and isinstance(docs_settings.TAGS, list):
            temp_schema["tags"] = docs_settings.TAGS
        
        if docs_settings.SERVERS["ADD"] is not None and isinstance(docs_settings.SERVERS["ADD"], list):
            temp_schema["servers"] = docs_settings.SERVERS["ADD"]
        elif docs_settings.SERVERS["ADD_CURRENT"]:
            temp_schema["servers"] = self._get_current_server()
        elif docs_settings.SERVERS["ADD_ALLOWED"]:
            temp_schema["servers"] = self._get_allowed_server()
        
        return temp_schema


    def _get_current_server(self):
        return [{
            "url": f"{self._req.scheme}://{self._req.get_host()}",
            "description": "Development server" if settings.DEBUG else "Production server"
        }]
    
    def _get_allowed_server(self):
        servers = settings.ALLOWED_HOSTS 
        return [{
            "url": f"{self._req.scheme}://{x}",
            "description": "Development server" if settings.DEBUG else "Production server"
        } for x in servers]


PARAM_PATTERN = re.compile(r'<(int|str):(\w+)>')

class PathSchemaGenerator:
    ep = APIEndpoint
    
    def __init__(self) -> None:
        self._endpoints = self.ep.get_endpoints(docs_settings.IGNORE_PATHS)
        self._path_schema=None
    
    @property
    def path_schema(self):
        if self._path_schema is None:
            self._path_schema = self._get_path_schema()
        return self._path_schema
    
    def _get_path_schema(self) -> dict:
        schema = {}
        for i, (path, methods) in enumerate(self._endpoints):
            inner = {}
            for method in methods:
                m = method.lower()
                inner[m] = {
                    "operationId": m + "PATH" + str(i),
                    "responses": {}
                }
            if self.has_params(path):
                inner["parameters"] = []
                for param, type_ in self.extract_params(path):
                    inner["parameters"].append({
                        "name": param,
                        "in": "path",
                        "required": True,
                        "style": "simple",
                        "schema": {
                            "type": type_
                        }
                    })
            
            schema[self.ep.format_endpoint(path)] = inner
        return schema

    def has_params(self, endpoint: str) -> bool:
        return "<" in endpoint

    def extract_params(self, endpoint: str) -> list[tuple[str, str]]:    
        # Find all params
        matches = PARAM_PATTERN.finditer(endpoint)
        
        params = []
        for match in matches:
            # Get the values
            type_ = match.group(1)
            param = match.group(2)
            
            # Map "int" or "str"
            if type_ == "int":
                mapped_type = "integer"
            elif type_ == "str":
                mapped_type = "string"
            
            # Add the mapped type and param value to the params list
            params.append((param, mapped_type))
        
        # Return the list of params
        return params




class ModelSchemaGenerator:
    def __init__(self) -> None:
        self._models = [x for x in apps.get_models() if x.__name__ not in docs_settings.IGNORE_MODELS]
        self._model_schema=None
    
    @property
    def model_schema(self):
        if self._model_schema is None:
            self._model_schema = self._get_model_schema()
        return self._model_schema
    
    
    def _get_model_schema(self):
        temp = {}
        for model in self._models:
            temp.update(self.create_model_schema(model))
        return temp
    
    
    def field_type_mapper(self, field) -> tuple[str, str]:
        if isinstance(field, (models.ForeignKey, models.ManyToManyField, models.ManyToManyField)):
            if isinstance(field.related_model, str):
                rel = field.related_model
            else:
                rel = field.related_model.__name__
            return None, rel
        if isinstance(field, (models.BigAutoField, models.PositiveBigIntegerField)):
            return "integer", None
        if isinstance(field, models.BooleanField):
            return "boolean", None
        if isinstance(field, models.DateTimeField):
            return "string", "date-time"
        if isinstance(field, models.EmailField):
            return "string", "email" 
        return "string", None
    
    def create_model_schema(self, model: models.Field):
        mn = model.__name__
        model_schema = {mn: {
            "type": "object",
            "required": [],
            "properties": {}
        }}
        fields = model._meta.local_fields
        for field in fields:
            type_ = self.field_type_mapper(field)
            name = field.name
            if not field.blank:
                model_schema[mn]["required"].append(name)
            if type_[0] is None:
                model_schema[mn]["properties"][name] = {"$ref": "#/components/schemas/" + type_[1]}
                continue
            model_schema[mn]["properties"][name] = {
                    "type": type_[0],
                    "nullable": field.null
                }
            
            for v in field.validators:
                if isinstance(v, MinLengthValidator):
                    model_schema[mn]["properties"][name]["minLength"] = v.limit_value

                if isinstance(v, MaxLengthValidator):
                    model_schema[mn]["properties"][name]["maxLength"] = v.limit_value

        return model_schema






def generate_schema(req):
    s = BaseSchemaGenerator(request=req).base_schema
    s["paths"] = PathSchemaGenerator().path_schema
    s["components"]["schemas"] = ModelSchemaGenerator().model_schema
    return s