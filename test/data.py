import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from engines.data_engine import Data

from pathlib import Path

# Get the current directory where the script is located
current_directory = Path(__file__).parent

# Create the log directory at the same level as the "engines" directory
download_directory = current_directory / "../downloads"
download_directory.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    data = Data()
    data.down_single_min_data('HK.00700', 6, download_directory)
