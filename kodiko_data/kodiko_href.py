import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
import json
from collections import OrderedDict



def login(driver, email, password, timesleep):
    
    # Click the login button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//span[@id='myAccountMenu']"))).click()
    url_to_connect = driver.find_element_by_xpath("//a[contains(text(),'Σύνδεση')]").get_attribute('href') #https://accounts.kodiko.gr/#/login?rapp=kodiko_legislation&rurl=https://www.kodiko.gr/
    driver.get(url_to_connect)
    time.sleep(2*timesleep)
    
    # Login using the credentials
    SELemail = driver.find_element_by_xpath("//input[@id='email_input']")
    SELpassword = driver.find_element_by_xpath("//input[@id='password_input']")
    SELemail.send_keys(email)
    time.sleep(2*timesleep)
    SELpassword.send_keys(password)
    time.sleep(2*timesleep)
    
    # Click on the Connect button
    driver.find_element_by_xpath("//button[contains(text(),'Συνδεση')]").click()
    time.sleep(2*timesleep)
    return driver


def main(url, email, password, timesleep, value=18):

    # Instantiate driver based on the landing_url
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Wait until Accept Conditions Button is visible and click
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
    time.sleep(timesleep)

    # Maximize the window
    driver.maximize_window()
    time.sleep(timesleep)

    # Login to the website using the given credentials
    driver = login(driver, email, password, timesleep)

    # Create the Dictionary that all the urls and titles will be stored
    data = OrderedDict()

    # Click the filter button and select the Category of Interest i.e "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ (Π.Δ.)" by the assigned value 18 (see Inspection for additional info)
    icon_filter = driver.find_element_by_class_name("icon-filter")
    icon_filter.click()
    time.sleep(timesleep)

    document_types = driver.find_element_by_xpath("//select[@id='document_types']")
    document_types.click()
    time.sleep(timesleep)
    sel = Select(document_types)
    sel.select_by_value("18")  # Alternative  #sel.select_by_visible_text("ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ (Π.Δ.)")

    # Iterate through the consecutive tabs until "Next" button is not available
    while True:    
        # Select the Element of Interest within the urls and titles will get extracted
        results = driver.find_elements_by_class_name("result")
        for ele in results:
            fullname = ele.find_element_by_class_name("fullname")
            atag = fullname.find_element_by_tag_name("a")
            href = atag.get_attribute('href')
            name = fullname.text
            try:
                text_muted = ele.find_element_by_class_name("text-muted")
                text = text_muted.text
            except:
                text = ''
            data[name] = [href, text]
        
        # Click on next tab
        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Επόμενο')]"))))
        except Exception as e:
            print(e)
            break

        time.sleep(3*timesleep)
        
    
    driver.close()
    return data

if __name__ == "__main__":
    landing_page = 'https://www.kodiko.gr/'
    email = 'christantonis.kons@gmail.com'
    password = '123456'
    timesleep = 1
    data = main(landing_page, email, password, timesleep, value=18)
    
    with open("kodiko_href.json", 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)








































