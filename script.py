##
## whatsapp_web_chat_link_format: "https://web.whatsapp.com/send?phone={}&text={}"
##

import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import pandas as pd
import platform
import sys
from os.path import expanduser
import argparse

def send_messages(message_urls, chrome_profile = "Default"):

    # keep track of status and write to csv at the end for future reference
    sending_status = []

    try:
        # chrome driver options
        chrome_options = Options()

        ## use a chrome profile where whatsapp web is logged in
        ## get chrome profile details by going to: chrome://version/

        # set chrome user data directory
        user_home_path = expanduser('~')
        if platform.system() == "Linux":
            chrome_options.add_argument(f"--user-data-dir={user_home_path}/.config/google-chrome/") # linux
        elif platform.system() == "Darwin":
            chrome_options.add_argument(f"--user-data-dir={user_home_path}/Library/Application Support/Google/Chrome/") # mac
        elif platform.system() == "Windows":
            chrome_options.add_argument(f"--user-data-dir={user_home_path}\\AppData\\Local\\Google\\Chrome\\User Data\\") # windows
        else:
            print("OS not recognized --> Exiting")
            sys.exit(1)
        # set chrome user profile name
        chrome_options.add_argument(f"--profile-directory={chrome_profile}")
        # make headless
        chrome_options.add_argument('--headless=new')

        # create chrome driver
        driver = webdriver.Chrome(options=chrome_options)

    except Exception as e:
        print("Error while creating chrome driver")
    
    try:
        # iterate over message urls and send messages
        for url in message_urls:
            print(f"Sending message <{url}>")

            try:
                driver.get(url)

                # wait till send button is loaded and click
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'))).click()

                
                # sleep for a while to avoid getting ip blocked due to large number of requests
                time.sleep(5)

                # sending status
                sending_status.append({
                    "url": url,
                    "status": "success"
                })
            except Exception as e:
                # sending status
                sending_status.append({
                    "url": url,
                    "status": "failed"
                })

                print(f"FailedToSend --> Skipping <{repr(e)}>")

                continue

    except Exception as e:
        if sending_status:
            write_log_to_csv(sending_status)
        print(f"Encountered exception while sending messages. <{repr(e)}>")
    else:
        if sending_status:
            write_log_to_csv(sending_status)
        print("All messages send --> Exiting")

def get_message_urls(input_excel):
    # read excel and return list of urls
    # assuming links are in column named 'Link'
    df = pd.read_excel(input_excel)['Link']

    return df.to_list()

def write_log_to_csv(list_of_dict, csv_filename = "sending_log.csv"):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, list_of_dict[0].keys())
        writer.writeheader()
        writer.writerows(list_of_dict)

if __name__ == "__main__":

    # get commandline arguments
    # Path(__file__).name
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--profile", help="Chrome profile where whatsapp web is logged in. Get profile name by going to chrome://version/", type=str)
    arg_parser.add_argument("--input_excel", help="Path to excel input containing links to send message.", type=str)
    # parse args
    args = arg_parser.parse_args()

    # input path
    input_excel = args.input_excel if args.input_excel else "recipients.xlsx"
    
    # get list of message urls from input excel
    message_urls = get_message_urls(input_excel)

    # send messages to urls
    if args.profile:
        send_messages(message_urls, chrome_profile=args.profile)
    else:
        send_messages(message_urls)
