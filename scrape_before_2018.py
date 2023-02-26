
import re
from bs4 import BeautifulSoup
import pandas as pd

from config import KEYWORDS

def scrapeBefore20180908(soup: BeautifulSoup, Date: str) -> pd.DataFrame:
    articles = soup.find_all('div',attrs={'class': lambda value: value and value.startswith('teaser')})

    articles_df=pd.DataFrame([], columns=['Date', 'Title','Statement','Link','Summary'])

    print(f'Found {len(articles)} SZ articles')

    for a in articles:
        # print('Found Story: ')
        # print(j.find("a",attrs={'class':'entry-title'}))
        Title = a.find("a",attrs={'class':'entry-title'}).find('strong').text.strip()
        Statement = a.find("a",attrs={'class':'entry-title'}).find('em').text.strip()
        Link = a.find("a",attrs={'class':'entry-title'})['href'].strip()
        Summary = a.find('p',attrs={'class':'entry-summary'}).text.strip()

        # check if a keyword is in the summary or title
        has_keyword = re.findall(KEYWORDS, Summary) or re.findall(KEYWORDS, Title) or re.findall(KEYWORDS, Statement)

        # if a keyword is found, append the row to the dataframe
        if (has_keyword):
            new_row = {'Date': Date, 'Title': Title, 'Statement': Statement, 'Link': Link, 'Summary': Summary}
            articles_df = articles_df.append(new_row, ignore_index=True)

            print('Extracted: ', new_row)

    return articles_df
