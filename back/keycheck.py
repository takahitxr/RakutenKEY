import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime

def Get_key():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.use_chromium = True


    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get('https://search.rakuten.co.jp/search/keyword/')

    req1 = browser.find_elements_by_class_name("kWdWrd")
    req2 = browser.find_elements_by_class_name("kWdRestWrd")

    req1.extend(req2)

    results = [
        {
        "keyword": key.text,
        "rank": a + 1
        }for a, key in enumerate(req1)
    ]

    return results