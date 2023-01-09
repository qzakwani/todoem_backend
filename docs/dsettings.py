from django.conf import settings

try:
    project = settings.DOCS_NAME
except AttributeError:
    project = settings.ROOT_URLCONF.split(".")[0].capitalize()
except:
    project = "PROJECT"

DEFAULTS = {
    "USE_GENERATED": False,
    "PUBLIC": False,
    "META": {
        "openapi": "3.0.3",
        "info": {
            "title": f"{project} API",
            "version": "1.0.0",
            "description": f"This is {project} API Docs.",
            "termsOfService": "http://example.com/terms/",
            "contact": {
                "name": f"{project} API Support",
                "url": f"http://www.{project.lower()}.com/support",
                "email": f"support@{project.lower()}.com"
            },
            "license": {
                "name": "OMAZ DOCS 2.0",
                "url": "omaz.xyz"
            },
        }
    },
    
    "MODELS_SCHEMA": False,
    
    "SERVERS": {
        "ADD_CURRENT": True,
        "ADD_ALLOWED": False,
        "ADD": None
        },
    "JWT_SECURITY": {
        "ADD": False,
        "ALL": False,
    },
    "DEFAULT_TAG": "Endpoints",
    "USE_TAGS": False,
    "TAGS_TYPE": "path", #path

    "IGNORE_MODELS": [
        "DocsSchema",
        "DocsSettings",
        "LogEntry",
        "Permission",
        "Group",
        "ContentType",
        "Session",
    ],
    
    "IGNORE_PATHS": [
        "docs/",
        "admin/",
    ],
    
    "LOGIN_URL": "admin:login",
    
    
    "UNAUTHORIZED_RESPONSE": {
    "openapi": "3.0.3",
        "info": {
            "title": f"{project} API",
            "version": "1.0.0",
            "description": f"Login Required for {project} API Docs.",

        },
        "paths": {}
        
    },
    "EMPTY_RESPONSE": {
    "openapi": "3.0.3",
        "info": {
            "title": f"{project} API",
            "version": "1.0.0",
            "description": f"Empty {project} API Docs.",

        },
        "paths": {}
    }
}





class DOCSSettings:
    """
    A settings object that allows DOCS settings to be accessed as
    properties. For example:

        from docs.settings import docs_settings
        print(api_settings.META)

    """
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'DOCS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid DOCS setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val



docs_settings = DOCSSettings(None, DEFAULTS)