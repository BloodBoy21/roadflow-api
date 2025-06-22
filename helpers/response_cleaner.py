
def clean_response(response):
    """
    Cleans the response by removing unnecessary whitespace and ensuring it is a string.
    
    Args:
        response (str or None): The response to clean.
        
    Returns:
        str: The cleaned response, or an empty string if the input was None.
    """
    if response is None:
        return ""

    response = response.strip().replace("\n", " ").replace("\r", " ")
    response = response.replace("```json", "").replace("```", "")
    return response.strip() if isinstance(response, str) else str(response).strip()
