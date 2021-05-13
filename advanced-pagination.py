from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests

ZILLOW_SEARCH = "https://www.zillow.com/homes/for_sale/house_type/2-_beds/2.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-123.96852293741617%2C%22east%22%3A-120.66163817179117%2C%22south%22%3A35.83888521067028%2C%22north%22%3A39.09055419111777%7D%2C%22mapZoom%22%3A8%2C%22customRegionId%22%3A%22c9752608c4X1-CRiubwbcg5jn26_xwnsy%22%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A1000000%7D%2C%22baths%22%3A%7B%22min%22%3A2%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3251%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdSbsAu1l2CdUagAH8MFD1UrPXckQITI_qOmcohsIYsb8CpYw/viewform?usp=sf_link"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}
CHROME_DRIVER = "/Users/david.cordero/Desktop/chromedriver"

page_num = 0

def make_soup(ZILLOW_SEARCH):
    response = requests.get(url=ZILLOW_SEARCH, headers=HEADERS)
    zillow_html = response.text
    soup = BeautifulSoup(zillow_html, "html.parser")

    #Get Prices
    prices = soup.find_all(class_="list-card-price")
    all_prices = [price.getText().split(" ")[0] for price in prices]

    #Get addresses
    addresses = soup.find_all(class_="list-card-addr")
    all_addresses = [add.text for add in addresses]

    #Get links
    links = soup.find_all(class_="list-card-link", href=True)
    all_links = [links[a]["href"] for a in range(0, len(links), 2)]

    return (all_prices, all_addresses, all_links)

def zillow_url():
    global page_num
    global ZILLOW_SEARCH
    if page_num == 0:
        ZILLOW_SEARCH = "https://www.zillow.com/homes/for_sale/house_type/2-_beds/2.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-123.96852293741617%2C%22east%22%3A-120.66163817179117%2C%22south%22%3A35.83888521067028%2C%22north%22%3A39.09055419111777%7D%2C%22mapZoom%22%3A8%2C%22customRegionId%22%3A%22c9752608c4X1-CRiubwbcg5jn26_xwnsy%22%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A1000000%7D%2C%22baths%22%3A%7B%22min%22%3A2%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3251%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
        page_num += 1
        return ZILLOW_SEARCH
    else:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER)
        driver.get(ZILLOW_SEARCH)
        time.sleep(2)
        next_button = driver.find_element_by_xpath("//a[@title='Next page']")
        next_button.click()
        time.sleep(2)
        ZILLOW_SEARCH = driver.current_url
        time.sleep(2)
        page_num += 1
        return ZILLOW_SEARCH



def fill_forms(all_prices, all_addresses, all_links):
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER)
    driver.get(GOOGLE_FORM)
    time.sleep(1)
    for x in range(0,40):
        fields = driver.find_elements_by_css_selector(".freebirdFormviewerComponentsQuestionTextTextInput .exportInput")
        address_field = fields[0]
        price_field = fields[1]
        link_field = fields[2]
        submit_button = driver.find_element_by_css_selector(".freebirdThemedFilledButtonM2")

        address_field.send_keys(f"{all_addresses[x]}")
        price_field.send_keys(f"{all_prices[x]}")
        link_field.send_keys(f"{all_links[x]}")

        submit_button.click()

        time.sleep(1)
        submit_another = driver.find_element_by_link_text("Submit another response")
        submit_another.click()
        time.sleep(1)

while page_num <10:
    tuple_var = make_soup(zillow_url())
    all_prices = tuple_var[0]
    all_addresses = tuple_var[1]
    all_links = tuple_var[2]
    time.sleep(2)
    fill_forms(all_prices, all_addresses, all_links)
    print(page_num)
    print(ZILLOW_SEARCH)

#
# driver.get(url=ZILLOW_SEARCH)
# next_button = driver.find_element_by_xpath("//*[@id='grid-search-results']/div[2]/nav/ul/li[10]/a")
# next_button.click()
# last_url = driver.current_url
#
# for x in range(0,7):
#     response = requests.get(url=last_url, headers=HEADERS)
#     zillow_html = response.text
#     soup = BeautifulSoup(zillow_html, "html.parser")
#
#     #Get Prices
#     prices = soup.find_all(class_="list-card-price")
#     all_prices = [price.getText().split(" ")[0] for price in prices]
#
#     #Get addresses
#     addresses = soup.find_all(class_="list-card-addr")
#     all_addresses = [add.text for add in addresses]
#
#     #Get links
#     links = soup.find_all(class_="list-card-link", href=True)
#     all_links = [links[a]["href"] for a in range(0, len(links), 2)]
#     last_url = driver.current_url
#     fill_forms()