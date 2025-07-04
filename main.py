import platform
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Create an MCP server
server = FastMCP("Screenshotter")


@server.tool()
def take_a_screenshot() -> str:
    """Take a screenshot and return the path to the saved file.

    This function supports macOS, Linux, and Windows platforms.
    Uses native screenshot tools for better performance and reliability.
    """
    # Get the current operating system
    current_os = platform.system().lower()

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        if current_os == "darwin":  # macOS
            # Use screencapture command
            temp_dir = Path(tempfile.gettempdir())
            screenshot_path = temp_dir / f"screenshot_{timestamp}.png"
            subprocess.run(
                ["screencapture", str(screenshot_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            return f"Screenshot saved successfully to: {screenshot_path}"

        elif current_os == "linux":  # Ubuntu/Linux
            # Use scrot command
            temp_dir = Path(tempfile.gettempdir())
            screenshot_path = temp_dir / f"screenshot_{timestamp}.png"

            # Check if scrot is available
            if not shutil.which("scrot"):
                return "Error: scrot command not found. Please install scrot: sudo apt-get install scrot"

            subprocess.run(
                ["scrot", str(screenshot_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            return f"Screenshot saved successfully to: {screenshot_path}"

        elif current_os == "windows":  # Windows
            # Use PowerShell with .NET commands
            temp_dir = Path(tempfile.gettempdir())
            screenshot_path = temp_dir / f"screenshot_{timestamp}.png"

            powershell_script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bitmap.Save("{screenshot_path}")
$graphics.Dispose()
$bitmap.Dispose()
"""

            subprocess.run(
                ["powershell", "-Command", powershell_script],
                capture_output=True,
                text=True,
                check=True,
            )
            return f"Screenshot saved successfully to: {screenshot_path}"

        else:
            return f"Error: Unsupported operating system: {current_os}"

    except subprocess.CalledProcessError as e:
        return f"Error taking screenshot: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


# Run the server
if __name__ == "__main__":
    print("Starting Screenshotter MCP server...")
    server.run()
