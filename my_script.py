# import packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
import sqlite3

#start new chrome browser
driver = webdriver.Chrome('C:/WebDrivers/chromedriver.exe')

#scraping the test page
url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
driver.get(url)
driver.maximize_window()

#find the caption of each product
products = driver.find_elements_by_class_name('caption')


# function to get the links of the products in each page
def add_id_and_name():
    links = {}
    #find the caption of each product in the first page
    products = driver.find_elements_by_class_name('caption')
    #loop through elements to get the links for each product
    for i in products:
        id_link = i.find_elements_by_tag_name('a')[0].get_attribute('href')
        links[id_link[-3:]] = i.find_elements_by_tag_name('a')[0].text
    return links

# get the pagination last page
pages_number = int(driver.find_element_by_class_name('pagination').text.split('\n')[-2])

#get the product links
product_links = {}
# loop through all pages to get the links
for _ in tqdm(range(pages_number), desc = 'Getting Required Links'):
    product_links.update(add_id_and_name()) #extend links in one list not lists inside list
    driver.find_elements_by_class_name('page-link')[-1].click()
    driver.maximize_window()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , 'col-md-9'))) # wait until page is loaded

driver.close()

print(product_links)
