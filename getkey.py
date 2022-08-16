import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import pandas as pd
import time
import datetime
import gspread
import json

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('angular-spider-312007-557058f7d529.json', scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1DNx5LcmrJyoxLKJM6qhasfM4CxlWOG9Yn1xmMUe2aDo'
sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート1')



def keycheck():

    url = "https://search.rakuten.co.jp/search/keyword/"

    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito')

    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    browser.get(url)
    browser.implicitly_wait(20)

    toprank = browser.find_elements_by_class_name("kWdWrd")
    nextrank = browser.find_elements_by_class_name("kWdRestWrd")
    toprank.extend(nextrank)

    results = {f"{i + 1}": key.text for i, key in enumerate(toprank)}
    
    browser.close()
    return results

data = sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

toprank = keycheck()
today = datetime.date.today().strftime("%Y/%m/%d")
toprank["Date"] = today
df = df.append(toprank, ignore_index=True)

set_with_dataframe(sheet, df, row=1, col=1)
