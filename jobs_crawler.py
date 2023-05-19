from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import csv
import re
from csv import writer
# Custom Logging
import logging
from webdriver_manager.core.logger import set_logger
# Handling Exception
from selenium.common.exceptions import NoSuchElementException


## Set Custom Logging ##
logger = logging.getLogger("upwork_helper_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler("upwork_helper.log"))

set_logger(logger)

## Set Chrome Driver Options ##

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_options.add_argument("--incognito")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--user-data-dir=C:/Users/Acer/AppData/Local/Google/Chrome/User Data')
# chrome_options.add_argument('--profile-directory=Profile 1'),
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless") # This won't show the window
chrome_options.page_load_strategy = 'normal'
# chrome_options.binary_location = "/usr/bin/google-chrome-stable"

print('Enter keyword: ')
keyword = input()

# url = f"https://www.upwork.com/nx/jobs/search/?q={keyword}&sort=recency" # without Login
url = f"https://www.upwork.com/nx/jobs/search/?q={keyword}&sort=recency" # with login

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
driver.add_cookie({"name":"cookie_domain", "value": ".upwork.com"})
driver.add_cookie({"name":"lang", "value": "en"})
driver.add_cookie({"name":"IR_gbd", "value": "upwork.com"})
time.sleep(30)

## Check if the Upwork website is reached out
logger.info(driver.title)

def jobs_crawler():
    counter = 0
    #open document and start writing process
    with open('./UpworkJobs.csv','w', encoding="utf-8", newline='') as fd:
        csv_writer = writer(fd, delimiter=",")
    
        # write title
        csv_writer.writerow([
                    'Job Title',
                    'Job link',
                    'Job Type',
                    'Fixed Salary',
                    'Work Load',
                    'Skills',
                    'Spent',
                    'Country',
                    'Payment Verification',
                    'Contractor Tier',
                    'Description'
                    ])
    
        # while True:
        logger.info("Page reading...")
        # wait content to be loaded
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[class='my-0 p-sm-right job-tile-title'] > a")))

        # detect next button
        # nextButton = driver.find_elements(By.CSS_SELECTOR, "button[class='up-pagination-item up-btn up-btn-link'] > div[class='next-icon up-icon']")

        # take web element
        jobCard = driver.find_elements(By.CSS_SELECTOR, "section[data-test='JobTile']")
        # write data to document
        for el in range(len(jobCard)):
            titleEls = jobCard[el].find_elements(By.CSS_SELECTOR, "h3[class='my-0 p-sm-right job-tile-title'] > a")
            typeEls = jobCard[el].find_elements(By.CSS_SELECTOR, "strong[data-test='job-type']")
            salaryEls = jobCard[el].find_elements(By.CSS_SELECTOR, "span[data-test='budget']")
            workLoadEls = jobCard[el].find_elements(By.CSS_SELECTOR, "span[data-test='duration']")
            contractorTierEls = jobCard[el].find_elements(By.CSS_SELECTOR, "span[data-test='contractor-tier']")
            skillTagEls = jobCard[el].find_elements(By.CSS_SELECTOR, "a[class='up-skill-badge text-muted'] > span")
            paymentEls = jobCard[el].find_elements(By.CSS_SELECTOR, "small[data-test='payment-verification-status'] > strong")
            spentEls = jobCard[el].find_elements(By.CSS_SELECTOR, "span[data-test='EarnedAmountFormatted'")
            countryEls = jobCard[el].find_elements(By.CSS_SELECTOR, "small[data-test='client-country'] > strong")
            descriptionEls = jobCard[el].find_elements(By.CSS_SELECTOR, "span[data-test='job-description-text']")

            csv_writer.writerow([
                titleEls[0].text if len(titleEls) else '',
                titleEls[0].get_attribute("href") if len(titleEls) else '',
                typeEls[0].text if len(typeEls) else '',
                salaryEls[0].text if len(salaryEls) else '',
                workLoadEls[0].text if len(workLoadEls) else '',
                ','.join((tag.text for tag in skillTagEls)), 
                spentEls[0].text if len(spentEls) else '',
                countryEls[0].text if len(countryEls) else '',
                paymentEls[0].text if len(paymentEls) else '',
                contractorTierEls[0].text if len(contractorTierEls) else '',
                descriptionEls[0].text if len(descriptionEls) else ''
                ])

        # detect next button disabled
        # if (len(nextButton) == 0):
        #     break          

        # move to next page
        # nextButton[0].click()
        # time.sleep(2)

#         counter += 1
#         logger.info('page: ' + str(counter))

#         if (counter == 2):
#             break