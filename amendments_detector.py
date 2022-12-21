from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from collections import OrderedDict
import argparse
import getpass
import time


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        values = getpass.getpass()
        setattr(namespace, self.dest, values)



def login(driver, email, password):
    
    # Click the login button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//span[@id='myAccountMenu']"))).click()
    url_to_connect = driver.find_element(by=By.XPATH, value="//a[contains(text(),'Σύνδεση')]").get_attribute('href') #https://accounts.kodiko.gr/#/login?rapp=kodiko_legislation&rurl=https://www.kodiko.gr/
    driver.get(url_to_connect)
    time.sleep(long_sleep/2)
    
    # Login using the credentials
    SELemail = driver.find_element(by=By.XPATH, value="//input[@id='email_input']")
    SELpassword = driver.find_element(by=By.XPATH, value="//input[@id='password_input']")
    SELemail.send_keys(email)
    time.sleep(long_sleep/2)
    SELpassword.send_keys(password)
    time.sleep(long_sleep/2)
    
    # Click on the Connect button
    driver.find_element(by=By.XPATH, value="//button[contains(text(),'Συνδεση')]").click()
    time.sleep(long_sleep/2)
    return driver


def main(driver, url):

    # Wait until Accept Conditions Button is visible and click
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
    driver.get(url)
    time.sleep(short_sleep)
    
    # Maximize the window
    #driver.maximize_window()
    time.sleep(short_sleep)
    
    body = driver.find_element(by=By.XPATH, value="//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul[1]")
    of_interest = body.find_elements(by=By.XPATH, value="//div[@title='Τροποποιήθηκε'] | //div[@title='Προστέθηκε']")
    clickables = []
    if not of_interest:
        return {}
    else:
        for elem in of_interest:
            clickables.append(elem.find_element("tag name", "span"))
    clickables = [x for x in clickables if "[-]" not in x.text]
        
    
    # Second approach to iterate on all clickables ~keep for now until finalize new selective approach :)
    # clickables = of_interest.find_elements("tag name", "span")
    # clickables = [x for x in clickables if "[-]" not in x.text]
    # clickables = [x for x in clickables if "Παρ" in x.text or "Άρθρο" in x.text]
    # clickables = [x for x in clickables if x.get_attribute("title") == "Τροποποιήθηκε"]
    #clickables = body.find_elements(by=By.XPATH, value="//div[@title='Τροποποιήθηκε'] | //div[@title='Προστέθηκε']")
    
    
    print(f"Available clickables {len(clickables)}")
 
    
    def get_text_after_clicking_amendment():
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='cod_info small text-muted'] a"))).click()
        time.sleep(short_sleep)
        text = driver.find_element(by=By.CSS_SELECTOR, value="div[id='myModal'] div[class='modal-body']").text
        driver.find_element(by=By.CSS_SELECTOR, value="div[id='myModal'] div[class='modal-footer'] button[type='button']").click()
        time.sleep(short_sleep)
        return text
    
    
    amendments = OrderedDict()
    for i in range(len(clickables)):
        time.sleep(short_sleep)
        clickables[i].click()
        time.sleep(short_sleep)
        
        ams = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='cod_info small text-muted'] a")
        if not ams:
            continue
        if len(ams) == 1:
            extracted_text = ams[0].text
            if extracted_text in amendments.keys():
                continue
            else:
                text = get_text_after_clicking_amendment()
                amendments[extracted_text] = text
        elif len(ams)>1:
            for am in ams:
                extracted_text = am.text
                if extracted_text in amendments.keys():
                    continue
                else:
                    text = get_text_after_clicking_amendment()
                    amendments[extracted_text] = text

        
    return amendments


if __name__ == "__main__":
    short_sleep, long_sleep = 1, 4
    
    parser = argparse.ArgumentParser(description="Retrieve Amendements from kodiko")
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--email', type=str, required=True)
    parser.add_argument('--password', action=Password, nargs='?', dest='password', required=True)
    parser.add_argument('--br', choices=["chrome", "firefox"], help="The browser to use")
    
    args = parser.parse_args()
    url = args.url
    email = args.email
    password = args.password
    browser = args.br
        
    # url = "https://www.kodiko.gr/nomothesia/document/308558"

    base_url = "https://www.kodiko.gr/"
    options = Options()
    options.page_load_strategy = 'eager'
    
    if browser == "chrome":
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    else:
        driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))
 
    driver.get(base_url)
    
    driver = login(driver, email, password)
    print("Successfully logged in. Now please wait this might take a while ...")
    results = main(driver, url)
    print(results.keys())
    
    






