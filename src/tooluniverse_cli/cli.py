#!/usr/bin/env python
"""
Main CLI module for ToolUniverse CLI.
"""
import sys
import json
import logging
import click
from rich.console import Console
from rich.table import Table
from tabulate import tabulate
from tooluniverse import ToolUniverse

from .commands.list_command import list_tools
from .commands.search_command import search_tools
from .commands.call_command import call_tool
from .commands.info_command import get_tool_info
from .utils import setup_logging, determine_category


console = Console()


@click.group()
@click.version_option()
@click.option('--verbose', is_flag=True, help='Show verbose output including tool loading information')
@click.pass_context
def cli(ctx, verbose):
    """ToolUniverse CLI - Access biomedical tools from the command line.
    
    This tool provides access to 214+ biomedical tools from FDA Drug Label data,
    OpenTargets, and Monarch Initiative.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    setup_logging(verbose)


@cli.command('list')
@click.option('--format', type=click.Choice(['text', 'json', 'table']), default='table', 
              help='Output format (table, text, or json)')
@click.option('--full-desc', is_flag=True, help='Show full tool description including all metadata')
@click.option('--category', type=str, help='Filter tools by category (e.g., "FDA", "OpenTarget", "Monarch")')
@click.pass_context
def list_cmd(ctx, format, full_desc, category):
    """List all available tools in ToolUniverse.
    
    Example usage:
      toolu list
      toolu list --category fda --format json
      toolu list --full-desc
    """
    list_tools(format=format, full_desc=full_desc, category=category, verbose=ctx.obj['verbose'])


@cli.command('search')
@click.argument('search_string')
@click.option('--format', type=click.Choice(['text', 'json', 'table']), default='table',
              help='Output format (table, text, or json)')
@click.option('--full-desc', is_flag=True, help='Show full tool description including all metadata')
@click.option('--category', type=str, help='Filter search results by category (e.g., "FDA", "OpenTarget", "Monarch")')
@click.option('--case-sensitive', is_flag=True, help='Perform case-sensitive search (default: case-insensitive)')
@click.pass_context
def search_cmd(ctx, search_string, format, full_desc, category, case_sensitive):
    """Search for tools with descriptions matching the search string.
    
    Example usage:
      toolu search "drug abuse"
      toolu search "phenotype" --category monarch --format json
      toolu search "HPO" --case-sensitive
    """
    search_tools(search_string, format=format, full_desc=full_desc, 
                 category=category, case_sensitive=case_sensitive, 
                 verbose=ctx.obj['verbose'])


@cli.command('info')
@click.argument('tool_name')
@click.option('--format', type=click.Choice(['text', 'json']), default='text',
              help='Output format (text or json)')
@click.pass_context
def info_cmd(ctx, tool_name, format):
    """Get detailed information about a specific tool.
    
    Example usage:
      toolu info get_drug_names_by_abuse_info
      toolu info get_phenotype_by_HPO_ID --format json
    """
    get_tool_info(tool_name, format=format, verbose=ctx.obj['verbose'])


@cli.command('call')
@click.argument('tool_name')
@click.argument('arguments', nargs=-1)
@click.option('--format', type=click.Choice(['text', 'json']), default='text',
              help='Output format (text or json)')
@click.pass_context
def call_cmd(ctx, tool_name, arguments, format):
    """Call a specific tool with arguments.
    
    Arguments should be provided in the format key=value.
    
    Example usage:
      toolu call get_drug_names_by_abuse_info abuse_type="misuse"
      toolu call get_phenotype_by_HPO_ID HPO_ID="HP:0001250" --format json
    """
    call_tool(tool_name, arguments, format=format, verbose=ctx.obj['verbose'])


def main():
    """Entry point for the CLI."""
    try:
        cli(obj={})
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
