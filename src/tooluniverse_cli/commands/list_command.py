"""
Implementation of the 'list' command.
"""
import json
import sys
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.style import Style
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

def list_tools(format='table', full_desc=False, category=None, verbose=False):
    """List all available tools in ToolUniverse.
    
    Args:
        format (str): Output format (table, text, or json).
        full_desc (bool): Whether to show full tool description.
        category (str): Category to filter by.
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
    
    # Create a list of tools with categories
    all_tools = []
    for name, desc in zip(tool_name_list, tool_desc_list):
        # Determine the category based on the tool name and description
        tool_category = determine_category(name, desc)
        
        # Clean up the description to remove redundant tool name
        clean_desc = desc
        if desc.startswith(name + ': '):
            clean_desc = desc[len(name) + 2:]
            
        all_tools.append((name, clean_desc, tool_category))
    
    # Filter by category if specified
    if category:
        filtered_tools = []
        for name, desc, tool_category in all_tools:
            if category.lower() in tool_category.lower():
                filtered_tools.append((name, desc, tool_category))
        all_tools = filtered_tools
    
    # Show tool count information (for non-JSON formats)
    tool_count = len(all_tools)
    if format != 'json':
        console.print(f"[bold]Total tools available:[/bold] {tool_count}")
    
    if not all_tools:
        console.print("[yellow]No tools found matching the specified criteria.[/yellow]")
        return
    
    if format == 'json':
        # Prepare JSON output
        tools_json = []
        for name, desc, tool_category in all_tools:
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
                    tools_json.append({
                        "name": name, 
                        "description": desc, 
                        "category": tool_category
                    })
            else:
                # For non-full-desc or non-JSON descriptions
                tools_json.append({
                    "name": name, 
                    "description": desc, 
                    "category": tool_category
                })
        
        # Use the utility function to format and output JSON
        metadata = {
            "total_tools": tool_count
        }
        format_json_output(tools_json, metadata)
    
    elif format == 'table':
        # Group tools by category
        categories = {}
        for name, desc, tool_category in all_tools:
            if tool_category not in categories:
                categories[tool_category] = []
            categories[tool_category].append((name, desc))
        
        # Use the utility function to print tools in a consistent format
        print_tools_by_category(categories)
    
    else:  # format == 'text'
        # Group tools by category
        categories = {}
        for name, desc, tool_category in all_tools:
            if tool_category not in categories:
                categories[tool_category] = []
            categories[tool_category].append((name, desc))
        
        # Print tools by category
        for category_name, tools in categories.items():
            console.print(f"\n[bold cyan]{category_name}[/bold cyan] ([bold]{len(tools)}[/bold] tools):")
            console.print("[dim]" + "-" * 52 + "[/dim]")
            console.print("[dim]" + "-" * 28 + "[/dim]")
            
            max_name_length = max(len(name) for name, _ in tools) if tools else 0
            for name, desc in tools:
                console.print(f"[bold green]{name}[/bold green]{' ' * (max_name_length - len(name) + 2)}{desc}")
