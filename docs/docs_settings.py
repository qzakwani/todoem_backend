from django.conf import settings

DEFAULTS = {
    "META": {
        "openapi": "3.0.3",
        "info": {
            "title": "DRF API",
            "version": "1.0.0"
        },
    },
    
    "SERVERS": {
        "ADD_CURRENT": True,
        "ADD_ALLOWED": False,
        "ADD": None
        },
    "JWT_SECURITY": {
        "ADD": False,
        "ALL": False,
    },
    
    "TAGS": None,

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