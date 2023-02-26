# sz-scraper
A **scraper for the german [Süddeutsche Zeitung](https://www.sueddeutsche.de)** using https://web.archive.org.

You can **search for articles that match *keywords* within a given *timeframe*.** The scraper will search for the keywords inside the article's *title*, *statement* and *summary* and save the article to `ARTICLES.csv` inside the `/data` directory.

The scraper **doesn't scrape the whole article** but only saves what's contained inside the *summary*, *title* and *statement* together with the *link* to the full article.

## Quickstart
### 1. Setup a virtual environment

###### 1.1. Install virtualenv
```shell
pip install virtualenv
```
###### 1.2.  Create a new environment
```shell
virtualenv ENV
```
###### 1.3. Activate it
```shell
source ENV/bin/activate
```
### 2.  Install requirements inside virtual environment
```shell
pip install -r requirements.txt
```
### 3. Start Scraper
```shell
python3 main.py
```
## Config File
Inside the `config.py` file you can adjust the following parameters:

`START_DATE` = The start date of the search

`END_DATE` = The end date of the search

`KEYWORDS`: Keywords to search for in the articles (regular expressions, e.g. `'AfD|Alternative für Deutschland'`) are allowed. More info [here](https://docs.python.org/3/library/re.html).

`FILENAME`: The name of the file to save the data to.

`USE_EXISTING_FILE`: Wether to use an existing file and append new rows to it or create a new one.

## 2018-09-08 Update:
On September 8, 2018, the HTML structure of SZ changed. Therefore, two different functions to extract articles exist. The script switches automatically.
