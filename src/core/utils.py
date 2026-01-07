import logging
import yaml
import os

def get_project_root():
    # Returns the root directory of the project (assuming src/core/utils.py)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_logging(name):
    root_dir = get_project_root()
    log_dir = os.path.join(root_dir, "src", "reports", "daily_reports")
    log_file = os.path.join(log_dir, "system.log")
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
    return logger

def load_config():
    root_dir = get_project_root()
    config_path = os.path.join(root_dir, "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
