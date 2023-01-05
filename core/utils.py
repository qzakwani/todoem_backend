from django.urls import get_resolver, URLResolver


def get_base_url(request) -> str:
    """
    Returns the base URL for the application based on the request object.
    
    Args:
        request: The request object.
        
    Returns:
        The base URL for the application.
    """
    return f"{request.scheme}://{request.get_host()}"



def get_urls() -> list[str]:
    """
    Returns a list of all urls
    
    #IMPOTANT: ignores list based urls like the default admin's
    """
    urls = []
    proj_urls = get_resolver().url_patterns
    for proj_url in proj_urls:
        url = str(proj_url.pattern._route)
        if isinstance(proj_url, URLResolver) and not isinstance(proj_url.urlconf_name, list):
            app_urls = proj_url.urlconf_name.urlpatterns
            for app_url in app_urls:
                urls.append(url + app_url.pattern._route)
        else:
            urls.append(url)
    return urls
