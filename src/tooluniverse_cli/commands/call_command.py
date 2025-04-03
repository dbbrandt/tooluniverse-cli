"""
Implementation of the 'call' command.
"""
import json
import sys
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
from tooluniverse import ToolUniverse
from ..utils import redirect_stdout_if_not_verbose, restore_stdout

console = Console()


def call_tool(tool_name, arguments, format='text', verbose=False):
    """Call a specific tool with arguments.
    
    Args:
        tool_name (str): Name of the tool to call.
        arguments (list): Tool arguments as a list of strings in the format key=value.
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
    
    # Parse arguments from command line
    tool_args = {}
    if arguments:
        for arg in arguments:
            try:
                key, value = arg.split("=", 1)
                tool_args[key] = value
            except ValueError:
                console.print(f"[bold red]Error:[/bold red] Argument '{arg}' is not in the format key=value")
                sys.exit(1)
    
    # Create query
    query = {"name": tool_name, "arguments": tool_args}
    
    # Only show call information in non-JSON mode
    if format != 'json':
        console.print(f"[bold]Calling tool:[/bold] [cyan]{tool_name}[/cyan]")
        if tool_args:
            console.print("[bold]With arguments:[/bold]")
            for key, value in tool_args.items():
                console.print(f"  [dim]{key}:[/dim] {value}")
        else:
            console.print("[bold]No arguments provided[/bold]")
        
        console.print()  # Empty line for better readability
    
    try:
        if format == 'json':
            # Redirect stdout during tool execution to suppress debug messages
            import io
            original_stdout = sys.stdout
            temp_stdout = io.StringIO()
            sys.stdout = temp_stdout
            
            # Call the tool with suppressed output
            result = tooluni.run(query, return_message=False, verbose=False)
            
            # Restore original stdout
            sys.stdout = original_stdout
            
            # Create structured JSON response with metadata
            json_response = {
                "metadata": {
                    "tool": tool_name,
                    "arguments": tool_args
                },
                "result": result
            }
            
            # Print JSON output without Rich formatting
            print(json.dumps(json_response, indent=2))
        else:
            # Call the tool with return_message=False to avoid debug info in output
            result = tooluni.run(query, return_message=False, verbose=verbose)
            
            # Format and display the result
            console.print(Panel("[bold green]Result:[/bold green]", expand=False))
            
            if isinstance(result, dict):
                # Handle dictionary results
                for key, value in result.items():
                    console.print(f"[bold]{key}:[/bold]")
                    
                    if isinstance(value, list):
                        # Handle list values
                        for i, item in enumerate(value):
                            if isinstance(item, dict):
                                # Print dictionaries as JSON
                                console.print(f"  [dim]Item {i+1}:[/dim]")
                                console.print(JSON(json.dumps(item)))
                            else:
                                console.print(f"  {item}")
                    elif isinstance(value, dict):
                        # Print dictionaries as JSON
                        console.print(JSON(json.dumps(value)))
                    else:
                        console.print(f"  {value}")
            elif isinstance(result, list):
                # Handle list results
                for i, item in enumerate(result):
                    if isinstance(item, dict):
                        # Print dictionaries as JSON
                        console.print(f"[dim]Item {i+1}:[/dim]")
                        console.print(JSON(json.dumps(item)))
                    else:
                        console.print(f"- {item}")
            else:
                # Handle simple results
                console.print(result)
    except Exception as e:
        console.print(f"[bold red]Error calling tool:[/bold red] {e}")
        sys.exit(1)
