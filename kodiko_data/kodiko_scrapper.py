import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd


def instantiateDriver(url='https://www.kodiko.gr/'):
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
    time.sleep(2)
    print("Good, I clicked the Accept button.")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//span[@id='myAccountMenu']"))).click()
    print("Good, I clicked the Sign-in button.")
    return driver

def login(driver):
    email, password = 'christantonis.kons@gmail.com', '123456'
    SELemail = driver.find_element_by_xpath("//input[@id='email_input']")
    SELpassword = driver.find_element_by_xpath("//input[@id='password_input']")
    SELemail.send_keys(email)
    time.sleep(2)
    SELpassword.send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath("//button[contains(text(),'Συνδεση')]").click()
    time.sleep(2)
    return driver
    

def main(urls_dict, login=False):
    driver = instantiateDriver()
    
    url_to_connect = driver.find_element_by_xpath("//a[contains(text(),'Σύνδεση')]").get_attribute('href') #https://accounts.kodiko.gr/#/login?rapp=kodiko_legislation&rurl=https://www.kodiko.gr/
    driver.get(url_to_connect)
    
    if login:
        driver = login(driver)
    
    time.sleep(2)
    for key in urls_dict:
        url = urls_dict[key]
        driver.get(url)
        
        # Scroll to the bottom
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        
        time.sleep(2)
        
        doc_relatives = []
        doc_rels = driver.find_elements_by_class_name("doc.relative")
        for ele in doc_rels:
            doc_relatives.append(ele.text)
    
    return doc_relatives


if __name__ == "__main__":
    login = True
    urls_dict = {
              "Υπουργείο Dummy": 'https://www.kodiko.gr/nomothesia/document/800098/p.d.-51-2022',
              "Υπουργείο Τουρισμού": 'https://www.kodiko.gr/nomothesia/document/308558'
             }

    data = main(urls_dict, login)
    









# tologin_email = 'christantonis.kons@gmail.com'
# tologin_password = '123456'

url = 'https://www.kodiko.gr/'
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)
driver.get(url)

# try:
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
#     print("Good, I clicked the Accept button.")
# except:
#     print("No Accept button to click. I continue")
#     pass

# time.sleep(2)
# #//span[@id='myAccountMenu']
# try:
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//span[@id='myAccountMenu']"))).click()
#     print("Good, I clicked the Accept button.")
# except:
#     print("No Accept button to click. I continue")
#     pass

# url_to_connect = driver.find_element_by_xpath("//a[contains(text(),'Σύνδεση')]").get_attribute('href') #https://accounts.kodiko.gr/#/login?rapp=kodiko_legislation&rurl=https://www.kodiko.gr/
# driver.get(url_to_connect)
# time.sleep(2)

# email = driver.find_element_by_xpath("//input[@id='email_input']")
# password = driver.find_element_by_xpath("//input[@id='password_input']")

# email.send_keys(tologin_email)
# password.send_keys(tologin_password)

# driver.find_element_by_xpath("//button[contains(text(),'Συνδεση')]").click()










urls_dict = {
              "Υπουργείο Dummy": 'https://www.kodiko.gr/nomothesia/document/800098/p.d.-51-2022',
              "Υπουργείο Τουρισμού": 'https://www.kodiko.gr/nomothesia/document/308558'
             }





for key in urls_dict:
    
    url = urls_dict[key]
    driver.get(url)
        
    # try:
    #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
    #     print("Good, I clicked the Accept button.")
    # except:
    #     print("No Accept button to click. I continue")
    #     pass
    
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(2)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    
    time.sleep(2)
    
    doc_relatives = []
    
    doc_rels = driver.find_elements_by_class_name("doc.relative")
    for ele in doc_rels:
        doc_relatives.append(ele.text)
    
    valid_doc_relatives = [x for x in doc_relatives if x]
    #valid_doc_relatives = valid_doc_relatives[:-1] # Consider if that applies for all cases

    chapters_idx = [idx for idx, val in enumerate(valid_doc_relatives) if val.lstrip().startswith("ΚΕΦΑΛΑΙΟ")]
    if len(chapters_idx)>1:
        chapters_idx.append(len(valid_doc_relatives))
        chapters = [valid_doc_relatives[previous:current] for previous, current in zip(chapters_idx, chapters_idx[1:])]
    else:
        chapters = []
    
    articles_idx = [idx for idx, val in enumerate(valid_doc_relatives) if 'Άρθρο' in val[:10]]
    if len(articles_idx)>1:
        articles_idx.append(len(valid_doc_relatives))
        articles = [valid_doc_relatives[previous:current] for previous, current in zip(articles_idx, articles_idx[1:])]
                
    
    
    
    