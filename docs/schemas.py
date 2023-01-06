
from rest_framework.schemas.generators import EndpointEnumerator
from .docs_settings import docs_settings, settings

class BaseDocsSchemaGenerator:
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
        self.endpoint_inspector = EndpointEnumerator()
    
    
    @property
    def base_schema(self) -> dict:
        if self._base_schema is None:
            self._base_schema = self.supply()
        return self._base_schema
    
    @property
    def endpoints(self):
        if self._endpoints is None:
            self._endpoints = self._get_endpoints()
        return self._endpoints
    
    
    def _get_endpoints(self):
        temp = {}
        res = self.endpoint_inspector.get_api_endpoints()
        for url, methods, _ in res:
            temp[url] = methods
        return temp
        
    
    def supply(self):
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



schema = BaseDocsSchemaGenerator

