import os
import pandas as pd
import logging
import shutil
from datetime import datetime
from api_client import ZipApiClient

class CSVProcessor:
    def __init__(self, config, mailer):
        paths_config = config.get("paths", {})
        self.input_folder = paths_config.get("input_folder", "input")
        self.output_folder = paths_config.get("output_folder", "output")
        self.archive_folder = paths_config.get("archive_folder", "archive")
        self.mailer = mailer
        self.api_client = ZipApiClient(config)

    def scan_and_process(self):
        logging.info("Scanning for new CSV files...")
        if not os.path.exists(self.input_folder):
            logging.error(f"Input folder '{self.input_folder}' does not exist.")
            return

        files = [f for f in os.listdir(self.input_folder) if f.endswith('.csv')]
        
        if not files:
            logging.info("No new CSV files found.")
            return
            
        for file in files:
            self.process_file(file)

    def process_file(self, filename):
        input_filepath = os.path.join(self.input_folder, filename)
        logging.info(f"Processing file: {filename}")
        
        try:
            df = pd.read_csv(input_filepath)
            
            # Check for required columns
            expected_cols = {'Zip', 'Email'}
            if not expected_cols.issubset(set(df.columns)):
                logging.error(f"File {filename} is missing required columns. Requires at least {expected_cols}")
                self.move_to_archive(filename)
                return

            # Add logic for processing each row
            states = []
            
            for index, row in df.iterrows():
                zip_code = str(row['Zip']).strip()
                email = str(row['Email']).strip()
                
                # Fetch state
                state_info = self.api_client.get_state_for_zip(zip_code)
                states.append(state_info)
                
                # Send email notation
                self.mailer.send_notification(email, zip_code, state_info)

            # Assign new column
            df['State'] = states
            
            # Save to output folder
            output_filename = f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            output_filepath = os.path.join(self.output_folder, output_filename)
            df.to_csv(output_filepath, index=False)
            logging.info(f"Successfully created output file: {output_filepath}")

            # Move to archive folder
            self.move_to_archive(filename)

        except Exception as e:
            logging.error(f"Error processing file {filename}: {e}")
            
    def move_to_archive(self, filename):
        src = os.path.join(self.input_folder, filename)
        dst = os.path.join(self.archive_folder, filename)
        
        # If file exists in archive, remove it so we can overwrite
        if os.path.exists(dst):
            os.remove(dst)
            
        shutil.move(src, dst)
        logging.info(f"Moved {filename} to archive.")
