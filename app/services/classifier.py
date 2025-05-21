"""
Incident classifier service module.

This module provides functionality to automatically classify incidents based on their description.
It uses a pre-trained LLM (Zero-Shot Classification) to determine the most appropriate category.
"""

from transformers import pipeline

# Initialize the zero-shot classifier (loads only once)
classifier = pipeline(
    "zero-shot-classification",
    model="joeddav/xlm-roberta-large-xnli",  # Multilingual model
    device="cpu"  # Use "cuda" if you have GPU
)

def classify_category(description: str) -> str:
    """
    Classify an incident into a category using a LLM-based zero-shot classifier.
    
    This function analyzes the incident description text and assigns a category
    using natural language understanding (no keyword matching required).
    
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
        >>> classify_category("I can't authenticate with my credentials")
        "Login Issue"
        >>> classify_category("The database is unresponsive")
        "Server Issue"
    """
    # Candidate categories (can be extended)
    candidate_labels = [
        "Network Issue",
        "Server Issue",
        "Software Issue",
        "Login Issue",
        "Other"
    ]
    
    # Get classification from the model
    result = classifier(description, candidate_labels, multi_label=False)
    
    # Return the highest-confidence label
    return result['labels'][0]