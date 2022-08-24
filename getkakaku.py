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
sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート3')
sheet4 = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート4')

def keycheck():

    url = "https://kakaku.com/keyword/"

    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito')

    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    browser.get(url)
    browser.implicitly_wait(20)

    req1 = browser.find_elements_by_class_name("wordListMain")
    keylist = req1[0].find_elements_by_tag_name('td')
    keylist2 = req1[1].find_elements_by_tag_name('td')
    keyres = []
    keyres2 = []
    res = [key.text for key in keylist]
    res2 = [key.text for key in keylist2]
    keyres.extend(res)
    keyres2.extend(res2)

    nextbutton = browser.find_elements_by_class_name("nextPage")

    while nextbutton:
        nextbutton[0].click()
        browser.implicitly_wait(10)
        req1 = browser.find_elements_by_class_name("wordListMain")
        keylist2 = req1[1].find_elements_by_tag_name('td')
        keylist = req1[0].find_elements_by_tag_name('td')
        res2 = [key.text for key in keylist2]
        res = [key.text for key in keylist]
        keyres2.extend(res2)
        keyres.extend(res)
        nextbutton = browser.find_elements_by_class_name("nextPage")

    results = {f"{i + 1}": key for i, key in enumerate(keyres)}
    results2 = {f"{i + 1}": key for i, key in enumerate(keyres2)}
    browser.close()
    return results, results2

data = sheet.get_all_values()
data2 = sheet4.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])
df2 = pd.DataFrame(data2[1:], columns=data[0])
toprank, toprank2 = keycheck()
today = datetime.date.today().strftime("%Y/%m/%d")
toprank["Date"] = today
toprank2["Date"] = today
df = df.append(toprank, ignore_index=True)
df2 = df2.append(toprank2, ignore_index=True)

set_with_dataframe(sheet, df, row=1, col=1)
set_with_dataframe(sheet4, df2, row=1, col=1)
