# Whatsapp Selenium Automation

## Requirements
  - Python 3.1x
  - Chrome browser

## Setting Up
  - Open chrome and login to Whatsapp web.
  - Install required python modules by running `pip install -r requirements.txt` inside the project directory.
  - Keep an excel file with message urls in 'Link' column *(preferably inside the same directory as the script and named recipients.xlsx)*.
  - Message Link format: `https://web.whatsapp.com/send?phone={}&text={}`
    - eg: `https://web.whatsapp.com/send?phone=9876543210&text=hello`

## Running the script
  - Run the script `python3 script.py`
  - Optional arguments:
    - `--profile` : Chrome profile where whatsapp web is logged in. Get profile name by going to chrome://version/
    - `--input_excel` : Path to excel input. If not provided, script checks for recipients.xlsx file in the same directory.
