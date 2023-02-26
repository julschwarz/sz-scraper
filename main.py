import sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd

from config import USE_EXISTING_FILE, KEYWORDS, FILENAME, START_DATE, END_DATE
from scrape_before_2018 import scrapeBefore20180908
from scrape_after_2018 import scrapeAfter20180908

#####################################
# SCRIPT TO PARSE SÜDDEUTSCHE ZEITUNG
#####################################

startDate = time.strptime(f'{START_DATE}', "%Y-%m-%d")
endDate = time.strptime(f'{END_DATE}', "%Y-%m-%d")

def main(startDate, endDate):
    # Set the current date to the start date
    currentDate = startDate

    # Create empty dataframe
    df=pd.DataFrame([], columns=['Date', 'Title','Statement','Link','Summary'])

    if USE_EXISTING_FILE:
        df = pd.read_csv(f'data/{FILENAME}')

    # Loop until the current date is greater than the end date
    while True:
        # Check if the current date is greater than the end date
        if currentDate > endDate:
            break
        currentDate = time.gmtime(time.mktime(currentDate) + 86400)

        print('processing date:', time.strftime("%d.%m.%Y", currentDate))
        url = f'https://web.archive.org/web/{time.strftime("%Y%m%d", currentDate)}/http://www.sueddeutsche.de/politik'
        print(url)

        #an exception might be thrown, so the code should be in a try-except block
        try:
            #use the browser to get the url.
            page=requests.get(url)

        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            print ('ERROR FOR LINK:',url)
            print (error_type, 'Line:', error_info.tb_lineno)
            continue

        time.sleep(2)
        soup=BeautifulSoup(page.text,'html.parser')

        # check if the date is before 2018-09-08 (the date when the website changed its structure)
        dateFormatted = time.strftime("%d.%m.%Y", currentDate)
        if (time.strftime("%Y%m%d", currentDate) < "20180908"):
            new_rows = scrapeBefore20180908(soup, dateFormatted)
        else:
            new_rows = scrapeAfter20180908(soup, dateFormatted)

        print(f'Added {len(new_rows)} articles that match keywords "{KEYWORDS}" on {dateFormatted}')
        print(f'----------------------------------------')

        # append new rows to dataframe
        df = pd.concat([df, new_rows], ignore_index=True)

        # Save to file:
        df.to_csv(f'data/{FILENAME}', index=False)

    # remove duplicates in the end
    df.drop_duplicates(subset=['Title', 'Statement'], inplace=True)
    df.to_csv(f'data/{FILENAME}', index=False)

    # print first 5 rows
    print(f'----------------------------------------')
    print(f'FINISHED: Found {len(df)} articles in total')
    print(f'----------------------------------------')
    print(df.head())

main(startDate, endDate)
