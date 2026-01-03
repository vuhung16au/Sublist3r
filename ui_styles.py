#!/usr/bin/env python3
# coding: utf-8
"""
UI Styles Configuration for Sublist3r
Centralized style configuration using Rich library for easy customization.
"""

from rich.console import Console
from rich.style import Style


class UIStyles:
    """Centralized style configuration for Sublist3r UI.
    
    This class provides easy-to-customize styles for all UI elements.
    To change colors, simply modify the style values below.
    """
    
    # Color styles - easily customizable
    SUCCESS = "green"      # Success messages, found subdomains
    WARNING = "yellow"     # Warning messages
    ERROR = "red"          # Error messages
    INFO = "blue"          # Informational messages
    BANNER = "red"         # Banner text color
    BANNER_SUBTITLE = "yellow"  # Banner subtitle color
    SOURCE = "cyan"        # Source/engine name color
    SUBDOMAIN = "green"    # Subdomain text color
    PORT = "yellow"        # Port number color
    RESET = "white"        # Default/reset color
    
    # Rich Style objects for advanced styling
    @classmethod
    def get_success_style(cls) -> Style:
        """Get success style."""
        return Style(color=cls.SUCCESS)
    
    @classmethod
    def get_warning_style(cls) -> Style:
        """Get warning style."""
        return Style(color=cls.WARNING)
    
    @classmethod
    def get_error_style(cls) -> Style:
        """Get error style."""
        return Style(color=cls.ERROR)
    
    @classmethod
    def get_info_style(cls) -> Style:
        """Get info style."""
        return Style(color=cls.INFO)
    
    @classmethod
    def get_banner_style(cls) -> Style:
        """Get banner style."""
        return Style(color=cls.BANNER, bold=True)
    
    @classmethod
    def get_source_style(cls) -> Style:
        """Get source/engine style."""
        return Style(color=cls.SOURCE)
    
    @classmethod
    def get_subdomain_style(cls) -> Style:
        """Get subdomain style."""
        return Style(color=cls.SUBDOMAIN)
    
    @classmethod
    def get_port_style(cls) -> Style:
        """Get port style."""
        return Style(color=cls.PORT)


# Global console instance - will be initialized in main script
_console = None


def get_console(no_color: bool = False) -> Console:
    """Get or create the global Rich console instance.
    
    Args:
        no_color: If True, disable colors in console output.
        
    Returns:
        Rich Console instance.
    """
    global _console
    if _console is None:
        _console = Console(no_color=no_color, force_terminal=True)
    return _console


def set_console(console: Console) -> None:
    """Set the global console instance.
    
    Args:
        console: Rich Console instance to use globally.
    """
    global _console
    _console = console


def reset_console() -> None:
    """Reset the global console instance (useful for testing)."""
    global _console
    _console = None

