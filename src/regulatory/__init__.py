import logging
import logging.config
from src.regulatory.utils.logger import log_config


LONG_DESCRIPTION = """
Regulatory AI Backend Project

This project initiates the AI backend development for the Design History File (DHF), focusing on the "Device Input" section. The backend is designed to streamline and automate regulatory documentation processes, leveraging AI to enhance efficiency and compliance.

Please refer to the attached PDF document for the detailed format and workflow specifications for the "Device Input" section. Review the document thoroughly before proceeding with further development.

Key Features:
- Modular AI backend architecture
- Support for regulatory documentation workflows
- Extensible design for future DHF sections

For more information, consult the project documentation or contact the StreamVision Team.
"""

# --- Version handling ---
try:
    from importlib.metadata import version
except ImportError:
    def version(distribution_name: str) -> str:
        return "0.0.1"

try:
    __version__ = version("regulatory")
except Exception:
    __version__ = "0.0.1"


# --- Metadata ---
__author__ = "StreamVision Team"
__license__ = "MIT"
__description__ = "AI backend services Regulatory AI Project."

def main() -> None:
    print("Hello from regulatory!")

# Use your named logger
logging.config.dictConfig(log_config)
logger = logging.getLogger("services")
logger.info(
    f"Regulatory AI Backend version: {__version__} - Regulatory AI is starting!"
)