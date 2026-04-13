# AI Prompt Logs

This file catalogs the main AI prompts used during the completion of this assignment.

## 1. Project Initialization & Scoping
**Prompt:**
> Create a Python application that reads a CSV file of zip codes and email addresses from a specific folder, retrieves the corresponding state information from the Zippopotam.us API (free API Endpoints), and writes the results to an output CSV file along with the zip code. The application also has a job that wakes up every 2 mins to scan the folder for new files and send a notification to email addresses provided for zip code in initial csv file. 

## 2. API Integration Generation
**Prompt:**
> Create a Python class `ZipApiClient` that will wrap requests to `http://api.zippopotam.us/us/{zip}` and handle exceptions. It should parse out the "state" element and the "state abbreviation".

## 3. Email Module Generation
**Prompt:**
> Implement an email sending module in Python using the `smtplib` and `email.message.EmailMessage`. It must accept standard config details such as `smtp_server`, `smtp_user`, and `smtp_password`. I need a mock or "simulate_email" flag for local testing purposes to log instead of send when the config flag is true.

## 4. Primary Processing Logic & File Manipulation
**Prompt:**
> Build a Python `CSVProcessor` class utilizing `pandas`. The processor should list all `.csv` files in the `input` directory. For each entry, extract the 'Zip' and 'Email', call the `ZipApiClient`, send a message using the email module, insert the state as a new 'State' column in the pandas dataframe, save to the `output` directory, and then move the processed csv file to an `archive` folder using `shutil`.

## 5. Scheduler Integration
**Prompt:**
> Write a `main.py` entrypoint. Use `schedule` module from Python. It needs an initial run at startup and then runs the CSVProcessor method every N minutes defined by a configuration file. Keep the script alive with a `while True` loop and `time.sleep`.
