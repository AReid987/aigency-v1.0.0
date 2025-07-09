#
 # File: config.py                                                             #
 # Project: xprt-commit                                                        #
 # Created Date: Fr Apr 2025                                                   #
 # Author: <<author>                                                           #
 # -----                                                                       #
 # Last Modified: Fri Apr 11 2025                                              #
 # Modified By: Antonio J. Reid                                                #
 # -----                                                                       #
 # Copyright (c) 2025 10xAigency                                               #
 # -----                                                                       #
 # HISTORY:                                                                    #
 # Date      	By	Comments                                                   #
 # ----------	---	---------------------------------------------------------  #




import tomllib
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Determine the project root relative to this file's location
# config.py is in packages/xprt-commit/src/xprt_commit/
# config.toml is in packages/xprt-commit/
CONFIG_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"

def load_config() -> Dict[str, Any]:
    """
    Loads and parses the configuration from the config.toml file.

    The config.toml file is expected to be located at the root of the
    'packages/xprt-commit' directory.

    Returns:
        A dictionary containing the configuration data. Returns an empty
        dictionary if the file is not found or cannot be parsed.
    """
    if not CONFIG_FILE_PATH.is_file():
        logger.error(f"Configuration file not found at: {CONFIG_FILE_PATH}")
        return {}

    try:
        with open(CONFIG_FILE_PATH, "rb") as f:
            config_data = tomllib.load(f)
            logger.info(f"Configuration loaded successfully from: {CONFIG_FILE_PATH}")
            return config_data
    except tomllib.TOMLDecodeError as e:
        logger.error(f"Error parsing TOML file {CONFIG_FILE_PATH}: {e}")
        return {}
    except OSError as e:
        logger.error(f"Error reading file {CONFIG_FILE_PATH}: {e}")
        return {}
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading config: {e}")
        return {}

# Example usage (optional, can be removed or placed under if __name__ == "__main__":)
# if __name__ == "__main__":
#     config = load_config()
#     if config:
#         print("Configuration loaded:")
#         import json
#         print(json.dumps(config, indent=2))
#     else:
#         print("Failed to load configuration.")