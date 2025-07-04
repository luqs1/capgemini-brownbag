"""
Alternative modern implementation using PIL (Pillow) for cross-platform screenshots.
This could be an option instead of platform-specific commands.
"""

from datetime import datetime
from pathlib import Path
import tempfile
from PIL import ImageGrab
from mcp.server.fastmcp import FastMCP

# Create an MCP server
server = FastMCP("Screenshotter")


@server.tool()
def take_a_screenshot_modern() -> str:
    """Take a screenshot using PIL/Pillow for cross-platform compatibility."""
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = Path(tempfile.gettempdir())
    screenshot_path = temp_dir / f"screenshot_{timestamp}.png"

    try:
        # Use PIL's ImageGrab which works on Windows and macOS
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        return f"Screenshot saved successfully to: {screenshot_path}"
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"


if __name__ == "__main__":
    print("Starting Modern Screenshotter MCP server...")
    server.run()
