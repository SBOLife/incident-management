"""
Incident classifier service module.

This module provides functionality to automatically classify incidents based on their description.
It uses keyword matching to determine the appropriate category for each incident.
"""

def classify_category(description) -> str:
    """
    Classify an incident into a category based on its description.
    
    This function analyzes the incident description text and assigns a category
    based on keyword matching. It performs case-insensitive matching against
    common terms associated with different types of incidents.
    
    Args:
        description (str): The incident description text to analyze.
        
    Returns:
        str: The determined incident category. One of:
            - "Network Issue": For network-related problems
            - "Server Issue": For server-related problems
            - "Software Issue": For software-related problems
            - "Login Issue": For authentication-related problems
            - "Other": For incidents that don't match any specific category
    
    Examples:
        >>> classify_category("The network connection is down")
        "Network Issue"
        >>> classify_category("Unable to log into the application")
        "Login Issue"
        >>> classify_category("Unknown problem occurred")
        "Other"
    """
    if "network" in description.lower():
        return "Network Issue"
    elif "server" in description.lower():
        return "Server Issue"
    elif "software" in description.lower():
        return "Software Issue"
    elif "login" in description.lower():
        return "Login Issue"
    else:
        return "Other"