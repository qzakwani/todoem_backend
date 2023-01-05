import re

PARAM_PATTERN = re.compile(r'<(int|str):(\w+)>')

def has_params(url: str) -> bool:
    return "<" in url

def extract_params(url: str) -> list[tuple[str, str]]:    
    # Find all the matches of the pattern in the string
    matches = PARAM_PATTERN.finditer(url)
    
    params = []
    for match in matches:
        # Get the values of "type" and "anyword"
        type_ = match.group(1)
        param = match.group(2)
        
        # Map "type" to "int" or "str"
        if type_ == "int":
            mapped_type = "integer"
        elif type_ == "str":
            mapped_type = "string"
        
        # Add the mapped type and param value to the params list
        params.append((mapped_type, param))
    
    # Return the list of params
    return params

def format_url(url: str) -> str:
    """
    format url to OpenAPI standards
    """
    formatted_url = url.replace("<int:", "{")
    formatted_url = formatted_url.replace("<str:", "{")
    formatted_url = formatted_url.replace(">", "}")
    return formatted_url

