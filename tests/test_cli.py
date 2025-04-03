"""
Unit tests for the CLI tool.
"""
import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from tooluniverse_cli.cli import cli


class TestCLI(unittest.TestCase):
    """Test cases for the CLI tool."""
    
    def setUp(self):
        """Set up the test environment."""
        self.runner = CliRunner()
    
    @patch('tooluniverse_cli.commands.list_command.ToolUniverse')
    def test_list_command(self, mock_tooluni):
        """Test the list command."""
        # Set up mock
        mock_instance = MagicMock()
        mock_tooluni.return_value = mock_instance
        mock_instance.refresh_tool_name_desc.return_value = (
            ["tool1", "tool2"], 
            ["Tool 1 Desc", "Tool 2 Desc"]
        )
        
        # Run command
        result = self.runner.invoke(cli, ['list'])
        
        # Verify output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Total tools available", result.output)
    
    @patch('tooluniverse_cli.commands.search_command.ToolUniverse')
    def test_search_command(self, mock_tooluni):
        """Test the search command."""
        # Set up mock
        mock_instance = MagicMock()
        mock_tooluni.return_value = mock_instance
        mock_instance.refresh_tool_name_desc.return_value = (
            ["tool_search", "another_tool"], 
            ["tool_search: A searchable tool", "another_tool: Another description"]
        )
        
        # Run command
        result = self.runner.invoke(cli, ['search', 'searchable'])
        
        # Verify output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Number of tools found", result.output)
    
    @patch('tooluniverse_cli.commands.info_command.ToolUniverse')
    def test_info_command(self, mock_tooluni):
        """Test the info command."""
        # Set up mock
        mock_instance = MagicMock()
        mock_tooluni.return_value = mock_instance
        mock_instance.get_one_tool_by_one_name.return_value = {
            'name': 'test_tool',
            'description': 'A test tool',
            'parameter': {
                'properties': {
                    'arg1': {
                        'type': 'string',
                        'required': True,
                        'description': 'Test argument'
                    }
                }
            }
        }
        
        # Run command
        result = self.runner.invoke(cli, ['info', 'test_tool'])
        
        # Verify output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("test_tool", result.output)
    
    @patch('tooluniverse_cli.commands.call_command.ToolUniverse')
    def test_call_command(self, mock_tooluni):
        """Test the call command."""
        # Set up mock
        mock_instance = MagicMock()
        mock_tooluni.return_value = mock_instance
        mock_instance.run.return_value = {"result": "success"}
        
        # Run command
        result = self.runner.invoke(cli, ['call', 'test_tool', 'arg1=value1'])
        
        # Verify output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Calling tool", result.output)


if __name__ == '__main__':
    unittest.main()
