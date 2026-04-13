# Zip Code Email Processor Application

This Python application reads CSV files containing Zip codes and email addresses, fetches the expected state for each Zip code from the Zippopotam.us API, generates an output CSV enriched with the state information, and sends a notification email to the listed addresses.

It features a background scheduling job that runs every 2 minutes automatically reading from the `input` directory. Processed files are moved to the `archive` directory to avoid reprocessing.

## Prerequisites

- Python 3.8+
- Active Internet connection (for API fetches and SMTP)

## Setup

1. **Install Dependencies**
   It's recommended to use a virtual environment.
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Configuration**
   Open `config.json` and configure your settings:
   - `input_folder`: Folder simulating the watch directory for new files.
   - `output_folder`: Processed CSVs will be placed here.
   - `archive_folder`: Folder holding completed original files.
   - `scheduler_interval_minutes`: How often the job wakes up to check the input folder (default: 2 mins).
   - `smtp_server`, `smtp_port`, `smtp_user`, `smtp_password`, `sender_email`: Configuration for sending the result notifications.
   - `simulate_email`: Boolean `true` or `false`. When `true`, it will only log the email to standard out and will not communicate with actual SMTP servers. Change to `false` when proper credentials are provided.

3. **Required Directories**
   The application generally expects `input`, `output`, and `archive` folders to exist next to the script. They have been configured and exist by default.

## Execution

To start the background listener and processing job, run:

```bash
python main.py
```

The script will begin watching the `input/` folder immediately and every 2 minutes thereafter.

## Input CSV Format
Ensure your CSV files have the following exact column headers to be processed correctly:
- `Zip`: The 5-digit US Zip code.
- `Email`: An email address to notify.
