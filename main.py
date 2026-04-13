import os
import time
import schedule
import logging
import yaml
from mailer import Mailer
from csv_processor import CSVProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def load_config():
    if not os.path.exists("config.yaml"):
        logging.error("config.yaml not found. Exiting.")
        return None
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def job(processor):
    processor.scan_and_process()

def main():
    config = load_config()
    if not config:
        return

    # Initialize components
    mailer = Mailer(config)
    processor = CSVProcessor(config, mailer)

    # Initial run before scheduling
    logging.info("Starting initial run...")
    job(processor)

    # Setup Schedule
    interval = config.get("scheduler", {}).get("interval_minutes", 2)
    logging.info(f"Scheduling job to run every {interval} minutes.")
    schedule.every(interval).minutes.do(job, processor)

    # Keep program running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
