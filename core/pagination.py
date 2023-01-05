from django.core.paginator import Paginator


################
## Paginator ###
################
def paginate_list(l, n: int, p: int=1):
    """
    Returns a paginated version of a list.
    
    Args:
        l: The list to paginate.
        n: The number of items to include on each page.
        p (optional): The page number to return. Default is 1.
        
    Returns:
        A page object containing the specified page of the paginated list.
    """
    paginator = Paginator(l, n) # Show n items per page.
    return paginator.get_page(p)