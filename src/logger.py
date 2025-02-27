import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs")  # Only Folder Path
os.makedirs(logs_path, exist_ok=True)          # Create Folder

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)  # Combine Folder and File Name

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s %(levelname)s - %(message)s",
    level=logging.INFO,
)



