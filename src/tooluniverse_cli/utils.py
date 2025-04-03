"""
Utility functions for the ToolUniverse CLI.
"""
import sys
import logging
from rich.console import Console

# Create a shared console instance with consistent styling for all commands to use
console = Console(highlight=True, force_terminal=True)


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


def format_json_output(data, metadata=None):
    """Format and print data as clean JSON without formatting escape sequences.
    
    This function handles creating a consistent JSON structure with metadata
    and ensures the output is clean without any ANSI escape sequences.
    
    Args:
        data: The main data to include in the JSON output.
        metadata (dict, optional): Metadata to include in the JSON output.
    """
    import json
    
    # Create a structured response with consistent format
    response = {}
    
    # Add metadata if provided
    if metadata:
        response["metadata"] = metadata
    
    # Add the main data with an appropriate key
    if isinstance(data, list):
        # For list data (like tools list or search results)
        response["tools"] = data
    else:
        # For other data types (like call results)
        response["result"] = data
    
    # Print clean JSON without Rich formatting
    print(json.dumps(response, indent=2))


def suppress_stdout_during_call(func, *args, **kwargs):
    """Execute a function with stdout suppressed to prevent debug output.
    
    Args:
        func: The function to call.
        *args: Arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
        
    Returns:
        The result of the function call.
    """
    import io
    import sys
    
    # Save original stdout
    original_stdout = sys.stdout
    
    # Redirect stdout to a dummy buffer
    temp_stdout = io.StringIO()
    sys.stdout = temp_stdout
    
    try:
        # Call the function
        result = func(*args, **kwargs)
        return result
    finally:
        # Restore original stdout
        sys.stdout = original_stdout


def format_tools_table(tools, category_name=None):
    """Create a formatted Rich table for displaying tools.
    
    Creates a consistent table format with horizontal separators between 
    tools and proper styling across all commands.
    
    Args:
        tools (list): List of (name, description) tuples to display.
        category_name (str, optional): Category name to include in the table title.
        
    Returns:
        rich.table.Table: Formatted table ready for printing.
    """
    from rich.table import Table
    
    # Create consistent table layout across all commands
    table = Table(
        show_header=True,
        header_style="bold magenta",
        row_styles=[""],  # Use default styling (black text)
        border_style="bright_black",
        padding=(0, 1),
        expand=True,
        show_lines=True  # Add horizontal lines between rows
    )
    
    # Add columns with consistent styling
    table.add_column("Tool Name", style="bold green", width=40, no_wrap=True)
    table.add_column("Description")  # Default black text for better readability
    
    # Add rows with proper wrapping
    for name, desc in tools:
        # Make sure description wraps properly
        wrapped_desc = desc.replace("\n", " ")
        table.add_row(name, wrapped_desc)
    
    return table


def print_tools_by_category(categories, show_tool_count=True, custom_console=None):
    """Print tools grouped by categories in a consistent format.
    
    Args:
        categories (dict): Dictionary mapping category names to lists of (name, description) tuples.
        show_tool_count (bool): Whether to show the tool count for each category.
        custom_console (rich.console.Console, optional): Custom console instance to use instead of
            the shared one. Rarely needed.
    """
    # Use the shared console by default, or a custom one if provided
    output_console = custom_console or console
    
    # Print tools by category
    for category_name, tools in categories.items():
        # Create category heading with tool count if requested
        if show_tool_count:
            output_console.print(f"\n[bold cyan]{category_name}[/bold cyan] ([bold]{len(tools)}[/bold] tools)")
        else:
            output_console.print(f"\n[bold cyan]{category_name}[/bold cyan]")
        
        # Format and print the table for this category
        table = format_tools_table(tools, category_name)
        output_console.print(table)
