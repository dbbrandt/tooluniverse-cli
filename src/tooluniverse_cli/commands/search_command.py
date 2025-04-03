"""
Implementation of the 'search' command.
"""
import json
from rich.table import Table
from tooluniverse import ToolUniverse
from ..utils import (
    determine_category, 
    redirect_stdout_if_not_verbose, 
    restore_stdout, 
    format_json_output,
    format_tools_table,
    print_tools_by_category,
    console
)

# No need to create a new console instance, using the shared one from utils


def search_tools(search_string, format='table', full_desc=False, 
                 category=None, case_sensitive=False, verbose=False):
    """Search for tools with descriptions matching the search string.
    
    Args:
        search_string (str): String to search for in tool names and descriptions.
        format (str): Output format (table, text, or json).
        full_desc (bool): Whether to show full tool description.
        category (str): Category to filter by.
        case_sensitive (bool): Whether to perform case-sensitive search.
        verbose (bool): Whether to show verbose output.
    """
    # Handle stdout redirection for non-verbose mode
    original_stdout = redirect_stdout_if_not_verbose(verbose)
    
    # Initialize and load tools
    tooluni = ToolUniverse()
    tooluni.load_tools()
    
    # Restore stdout if we redirected it
    restore_stdout(original_stdout)
    
    # Get tool names and descriptions
    tool_name_list, tool_desc_list = tooluni.refresh_tool_name_desc(enable_full_desc=full_desc)
    
    # Clean up descriptions and prepare the search results
    search_results = []
    for name, desc in zip(tool_name_list, tool_desc_list):
        # Clean up the description
        clean_desc = desc
        if desc.startswith(name + ': '):
            clean_desc = desc[len(name) + 2:]
            
        # Get searchable text for matching
        searchable_text = name + " " + clean_desc
        
        # For full JSON descriptions, also search within the parsed JSON if possible
        if full_desc and desc.startswith('{'):
            try:
                json_desc = json.loads(desc)
                if "description" in json_desc:
                    searchable_text += " " + json_desc["description"]
            except json.JSONDecodeError:
                pass
        
        # Check if the search string is in the name or description
        if case_sensitive:
            is_match = search_string in searchable_text
        else:
            is_match = search_string.lower() in searchable_text.lower()
            
        if is_match:
            # Determine the category based on the tool name and description
            tool_category = determine_category(name, clean_desc)
            search_results.append((name, desc, tool_category))
    
    # Filter by category if specified
    if category:
        filtered_results = []
        for name, desc, tool_category in search_results:
            if category.lower() in tool_category.lower():
                filtered_results.append((name, desc, tool_category))
        search_results = filtered_results
    
    # Always calculate search result count
    results_count = len(search_results)
    
    # Show count only in non-JSON formats
    if format != 'json':
        console.print(f"[bold]Number of tools found matching '[cyan]{search_string}[/cyan]':[/bold] {results_count}")
    
    if not search_results:
        console.print("[yellow]No tools found matching the search criteria.[/yellow]")
        return
    
    if format == 'json':
        # Prepare JSON output
        tools_json = []
        for name, desc, tool_category in search_results:
            # If full_desc is enabled and the description is a JSON string, parse it
            if full_desc and desc.startswith('{'):
                try:
                    # Parse the full description and add it directly to tools list
                    tool_json = json.loads(desc)
                    
                    # Add category to the JSON object
                    tool_json["category"] = tool_category
                    tools_json.append(tool_json)
                except json.JSONDecodeError:
                    # Fallback if parsing fails
                    clean_desc = desc
                    if desc.startswith(name + ': '):
                        clean_desc = desc[len(name) + 2:]
                    tools_json.append({
                        "name": name, 
                        "description": clean_desc, 
                        "category": tool_category
                    })
            else:
                # For non-full-desc or non-JSON descriptions
                clean_desc = desc
                if desc.startswith(name + ': '):
                    clean_desc = desc[len(name) + 2:]
                tools_json.append({
                    "name": name, 
                    "description": clean_desc, 
                    "category": tool_category
                })
        
        # Create a complete JSON response with metadata
        metadata = {
            "query": search_string,
            "total_results": results_count
        }
        
        # Use the utility function to format and output JSON
        format_json_output(tools_json, metadata)
    
    elif format == 'table':
        # Group search results by category
        categories = {}
        for name, desc, tool_category in search_results:
            if tool_category not in categories:
                categories[tool_category] = []
            
            # Clean up the description for display
            clean_desc = desc
            if desc.startswith(name + ': '):
                clean_desc = desc[len(name) + 2:]
                
            categories[tool_category].append((name, clean_desc))
        
        # Use the utility function to print tools in a consistent format
        print_tools_by_category(categories)
    
    else:  # format == 'text'
        # Group search results by category
        categories = {}
        for name, desc, tool_category in search_results:
            if tool_category not in categories:
                categories[tool_category] = []
            
            # Clean up the description for display
            clean_desc = desc
            if desc.startswith(name + ': '):
                clean_desc = desc[len(name) + 2:]
                
            categories[tool_category].append((name, clean_desc))
        
        # Print search results by category
        for category_name, tools in categories.items():
            console.print(f"\n[bold]{category_name}[/bold] ({len(tools)} tools):")
            console.print("-" * 80)
            
            max_name_length = max(len(name) for name, _ in tools)
            for name, desc in tools:
                console.print(f"{name.ljust(max_name_length + 2)}{desc}")
