
import re
from bs4 import BeautifulSoup
import pandas as pd

from config import KEYWORDS

def scrapeAfter20180908(soup: BeautifulSoup, Date: str) -> pd.DataFrame:
    articles = soup.find_all('a',attrs={'class': lambda value: value and value.startswith('sz-teaser')})

    articles_df=pd.DataFrame([], columns=['Date', 'Title','Statement','Link','Summary'])

    print(f'Found {len(articles)} SZ articles')

    for a in articles:
        try:
            # print('Found Story: ')
            # print(j.find("a",attrs={'class':'entry-title'}))
            Title = a.find("div",attrs={'class':'sz-teaser__overline-title'}).text.strip()
            Statement = a.find(attrs={'class':'sz-teaser__title'}).text.strip()
            Link = a['href'].strip()
            Summary = a.find('p',attrs={'class':'sz-teaser__summary'}).text.strip()

            # check if a keyword is in the summary or title
            has_keyword = re.findall(KEYWORDS, Summary) or re.findall(KEYWORDS, Title) or re.findall(KEYWORDS, Statement)

            # if a keyword is found, append the row to the dataframe
            if (has_keyword):
                new_row = {'Date': Date, 'Title': Title, 'Statement': Statement, 'Link': Link, 'Summary': Summary}
                articles_df = articles_df.append(new_row, ignore_index=True)
                print('Extracted: ', new_row)
        except:
            print ('ERROR FOR ARTICLE:',a)
            continue

    return articles_df
