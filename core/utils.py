def get_base_url(request) -> str:
    """
    Returns the base URL for the application based on the request object.
    
    Args:
        request: The request object.
        
    Returns:
        The base URL for the application.
    """
    return f"{request.scheme}://{request.get_host()}"