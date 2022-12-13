from django.core.paginator import Paginator


################
## Paginator ###
################
def paginate_list(l, n: int, p: int=1):
    paginator = Paginator(l, n) # Show n items per page.
    return paginator.get_page(p)