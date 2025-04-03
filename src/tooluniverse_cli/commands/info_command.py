"""
Implementation of the 'info' command.
"""
import json
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from tooluniverse import ToolUniverse
from ..utils import redirect_stdout_if_not_verbose, restore_stdout

console = Console()


def get_tool_info(tool_name, format='text', verbose=False):
    """Get detailed information about a specific tool.
    
    Args:
        tool_name (str): Name of the tool to get information about.
        format (str): Output format (text or json).
        verbose (bool): Whether to show verbose output.
    """
    # Handle stdout redirection for non-verbose mode
    original_stdout = redirect_stdout_if_not_verbose(verbose)
    
    # Initialize and load tools
    tooluni = ToolUniverse()
    tooluni.load_tools()
    
    # Restore stdout if we redirected it
    restore_stdout(original_stdout)
    
    # Get tool information
    tool = tooluni.get_one_tool_by_one_name(tool_name, return_prompt=True)
    
    if not tool:
        console.print(f"[bold red]Error:[/bold red] Tool '[bold]{tool_name}[/bold]' not found")
        sys.exit(1)
    
    if format == 'json':
        # Print tool information as JSON without Rich formatting
        print(json.dumps(tool, indent=2))
    else:
        # Print tool information in a structured format
        console.print(Panel(f"[bold cyan]{tool['name']}[/bold cyan]", 
                            title="Tool Information", expand=False))
        
        console.print("\n[bold]Description:[/bold]")
        console.print(tool['description'])
        
        console.print("\n[bold]Parameters:[/bold]")
        if 'parameter' in tool and 'properties' in tool['parameter']:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Parameter", style="dim")
            table.add_column("Type")
            table.add_column("Required")
            table.add_column("Description")
            
            for param_name, param_info in tool['parameter']['properties'].items():
                required = param_info.get('required', False)
                req_text = "Yes" if required else "No"
                param_type = param_info.get('type', 'unknown')
                desc = param_info.get('description', 'No description')
                
                table.add_row(param_name, param_type, req_text, desc)
            
            console.print(table)
        else:
            console.print("  No parameters defined")
        
        # Show additional information if available
        if 'label' in tool:
            console.print("\n[bold]Labels:[/bold]")
            console.print(", ".join(tool['label']))
            
        if 'type' in tool:
            console.print("\n[bold]Type:[/bold]")
            console.print(tool['type'])
