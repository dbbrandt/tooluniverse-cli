"""
Utility functions for the ToolUniverse CLI.
"""
import sys
import logging
from rich.console import Console

console = Console()


def setup_logging(verbose=False):
    """Set up logging configuration.
    
    Args:
        verbose (bool): Whether to enable verbose logging.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()] if verbose else []
    )


def redirect_stdout_if_not_verbose(verbose):
    """Redirect stdout to /dev/null if not verbose.
    
    Args:
        verbose (bool): Whether output is verbose.
        
    Returns:
        original_stdout: The original stdout if redirected, None otherwise.
    """
    if not verbose:
        original_stdout = sys.stdout
        sys.stdout = open('/dev/null', 'w')
        return original_stdout
    return None


def restore_stdout(original_stdout):
    """Restore stdout if it was redirected.
    
    Args:
        original_stdout: The original stdout to restore, or None if not redirected.
    """
    if original_stdout:
        sys.stdout.close()
        sys.stdout = original_stdout


def determine_category(name, desc):
    """Determine the category of a tool based on its name and description.
    
    Args:
        name (str): Tool name.
        desc (str): Tool description.
        
    Returns:
        str: The category name.
    """
    # Check known special tools first
    if name in ["Finish", "Tool_RAG", "CallAgent"]:
        return "Special Tools"
    
    # FDA Drug Label Tools
    if "drug" in name.lower():
        return "FDA Drug Label Tools"
    
    # Monarch Tools - broader criteria
    if any(term in name.lower() or term in desc.lower() for term in [
        "phenotype", "hpo", "monarch", "joint_associated", "symptom"
    ]):
        return "Monarch Tools"
        
    # OpenTarget Tools - must check after more specific categories
    if any(term in name.lower() for term in [
        "target", "disease", "gene", "ensembl", "efo"
    ]):
        return "OpenTarget Tools"
    
    return "Special Tools"


def format_tool_for_display(name, description, category=None, **kwargs):
    """Format a tool for display.
    
    Args:
        name (str): Tool name.
        description (str): Tool description.
        category (str, optional): Tool category.
        **kwargs: Additional tool properties.
        
    Returns:
        dict: Formatted tool information.
    """
    tool_info = {
        "name": name,
        "description": description
    }
    
    if category:
        tool_info["category"] = category
        
    # Add any additional properties
    for key, value in kwargs.items():
        if value is not None:
            tool_info[key] = value
            
    return tool_info
