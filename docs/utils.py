from django.urls import get_resolver, URLResolver, URLPattern
from rest_framework.views import APIView

class APIEndpoint:
    @classmethod
    def get_endpoints(cls, ignore: None|list) -> list[tuple[str,tuple[str]]]:
        """
        Returns a list of all endpoints that conform to DRF APIView
        
        #IMPOTANT: - ignores list based urls like the default admin's
                    - depth of urls is 1 -> ignores inclueed urls inside apps
        """
        urls = []
        proj_urls = get_resolver().url_patterns
        for proj_url in proj_urls:
            url = str(proj_url.pattern._route)
            if isinstance(proj_url, URLResolver) and not isinstance(proj_url.urlconf_name, list):
                app_urls = proj_url.urlconf_name.urlpatterns
                for app_url in app_urls:
                    if isinstance(app_url, URLPattern) and cls._is_drf_endpoint(app_url.callback):
                        temp = url + str(app_url.pattern._route)
                        if ignore is not None:
                            for i in ignore:
                                if temp.startswith(i):
                                    continue
                        urls.append((temp, cls._get_methods(app_url.callback)))
            elif isinstance(proj_url, URLPattern) and cls._is_drf_endpoint(proj_url.callback):
                if ignore is not None:
                            for i in ignore:
                                if temp.startswith(i):
                                    continue
                urls.append((url, cls._get_methods(proj_url.callback)))
        return urls
    
    @classmethod
    def _is_drf_endpoint(cls, callback):
        _cls = getattr(callback, "cls", None)
        return (_cls is not None) and issubclass(_cls, APIView)

    @classmethod
    def _get_methods(cls, callback) -> tuple[str]:
        methods = callback.cls().allowed_methods
        return (method for method in methods if method not in ('OPTIONS', 'HEAD'))

    @staticmethod
    def format_endpoint(endpoint: str) -> str:
        """
        format endpoint to OpenAPI standards
        """
        formatted_endpoint = endpoint.replace("<int:", "{")
        formatted_endpoint = formatted_endpoint.replace("<str:", "{")
        formatted_endpoint = formatted_endpoint.replace(">", "}")
        if formatted_endpoint[-1] == '/':
            formatted_endpoint = formatted_endpoint[:-1]
        if formatted_endpoint[0] != '/':
            formatted_endpoint = '/' + formatted_endpoint
        return formatted_endpoint






