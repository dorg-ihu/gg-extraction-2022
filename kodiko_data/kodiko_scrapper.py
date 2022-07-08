import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import json
from collections import OrderedDict


def make_split_on_webelements(thelist, identifier='Άρθρο'):
    """
    list of webelements
    """
    if len(thelist) == 0:
        return []
    r0, r1 = [], []
    for s in thelist:
        if identifier in s.text:
            if r1:
                r0.append(r1)
                r1 = []
        r1.append(s)
    return r0 + [r1]

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
    



url = 'https://www.kodiko.gr/'
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)
driver.get(url)


urls_dict = {
              "Υπουργείο Dummy": 'https://www.kodiko.gr/nomothesia/document/800098/p.d.-51-2022',
              "Υπουργείο Τουρισμού": 'https://www.kodiko.gr/nomothesia/document/308558'
             }


for key in urls_dict:
    
    url = urls_dict[key]
    driver.get(url)
        
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
  

              
#%%


import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import json
from collections import OrderedDict

def make_split_on_webelements(thelist, identifier='Άρθρο'):
    """
    list of webelements
    """
    if len(thelist) == 0:
        return []
    r0, r1 = [], []
    for s in thelist:
        if identifier in s.text:
            if r1:
                r0.append(r1)
                r1 = []
        r1.append(s)
    return r0 + [r1]


urls_dict = {
              "Υπουργείο Dummy": 'https://www.kodiko.gr/nomothesia/document/800098/p.d.-51-2022',
              "Υπουργείο Τουρισμού": 'https://www.kodiko.gr/nomothesia/document/308558'
             }





# for key in urls_dict:
    
#     url = urls_dict[key]
#     driver.get(url)
timesleep = 0.5

#url = 'https://www.kodiko.gr/nomothesia/document/308558'
#url = 'https://www.kodiko.gr/nomothesia/document/800098/p.d.-51-2022'
url = 'https://www.kodiko.gr/nomothesia/document/800076/p.d.-49-2022'
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)
driver.get(url)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
time.sleep(timesleep)
document = OrderedDict()
time.sleep(2)

identifier = driver.find_element_by_css_selector("h1[class='center left-md']")
IDENTITY = identifier.text



HEADER = driver.find_element_by_xpath("//span[contains(text(),'Κεφαλίδα')]")
HEADER.click()
time.sleep(timesleep)

header_content = driver.find_element_by_class_name("dc_srch_trgt")

TITLE = header_content.find_elements_by_tag_name("p")[1].text

prereq = header_content.text
prereq_idx = prereq.find("Έχοντας υπόψη")
PREREQ = prereq[prereq_idx:].replace("\n", " ")

BODY = driver.find_element_by_xpath("//span[contains(text(),'Σώμα')]")
BODY.click()
time.sleep(timesleep)


chapters_exist = False
inner_body = driver.find_elements_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul/li")
for ele in inner_body:
    if "ΚΕΦΑΛΑΙΟ" in ele.text:
        chapters_exist = True
        break

if not chapters_exist:
    articles = OrderedDict()
    for ele in inner_body:
        article_clickables = ele.find_elements_by_tag_name("span")
        article_clickables[0].click()
        time.sleep(timesleep)
        
        article_title_element = driver.find_element_by_class_name("doc.relative")
        article_title_tag = article_title_element.find_element_by_class_name("center").text
        try:
            article_title_text = article_title_element.find_element_by_class_name("center.dc_srch_trgt").text
        except:
            article_title_text = ''
        if article_title_text:
            article_title = article_title_tag + ' - ' + article_title_text
        else:
            article_title = article_title_tag
        
        if len(article_clickables) == 1:
            article_body = driver.find_elements_by_tag_name("p")
            text = [x.text for x in article_body if x.text]
            article_text = " ".join(text)
            articles[article_title] = article_text
        elif len(article_clickables) > 1:
            article_clickables = [x for x in article_clickables if x.text != "[-]"]
            paragraphs = OrderedDict()
            for i in range(1, len(article_clickables)):
                article_clickables[i].click()
                time.sleep(timesleep)
                text = driver.find_element_by_class_name("dc_srch_trgt").text
                paragraphs[i] = text
            articles[article_title] = paragraphs
            #clickables = [x for x in clickables if "Άρθρο" not in x.text]
    document["body"] = articles
else:
    chapters = OrderedDict()
    for ele in inner_body:
        ele = inner_body[0]
        initial_body = ele.find_element_by_class_name("pointer").click()
        
        if initial_body is None:
            articles = ele.find_elements_by_tag_name("li")
        
        initial_title = initial_body.text
        time.sleep(timesleep)
        initial_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
        print(initial_title)
        
        chapter_content = ele.find_element_by_tag_name("ul")
        

        
        chapter_clickables = ele.find_elements_by_tag_name("span")
        chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
        chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
        
        chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
          
        articles = OrderedDict()
        for artcl in chapter_articles_and_paragraphs:
            
            artcl[0].click()
            time.sleep(timesleep)
            
            article_title_element = driver.find_element_by_class_name("doc.relative")
            article_title_tag = article_title_element.find_element_by_class_name("center").text
            try:
                article_title_text = article_title_element.find_element_by_class_name("center.dc_srch_trgt").text
            except:
                article_title_text = ''
            if article_title_text:
                article_title = article_title_tag + ' - ' + article_title_text
            else:
                article_title = article_title_tag
    
            if len(artcl) == 1:
                article_body = driver.find_elements_by_tag_name("p")
                text = [x.text for x in article_body if x.text]
                article_text = " ".join(text)
                articles[article_title] = article_text
            elif len(artcl) > 1:
                paragraphs = OrderedDict()
                for i in range(1, len(artcl)):
                    artcl[i].click()
                    time.sleep(timesleep)
                    text = driver.find_element_by_class_name("dc_srch_trgt").text
                    paragraphs[i] = text
                articles[article_title] = paragraphs
            time.sleep(timesleep)
    
        chapters[initial_title] = articles
        
    document["body"] = chapters

document["identity"] = IDENTITY
document["title"] = TITLE
document["prereq"] = PREREQ
#document["body"] = chapters


documents_json = json.dumps(document)
with open("kodiko_data.json", 'w', encoding='utf-8') as fp:
    json.dump(document, fp, ensure_ascii=False)

    
with open("kodiko_data.json", "r", encoding='utf-8') as s:
    data = json.load(s)





















for ele in inner_body:
    
    chapter_body = ele.find_element_by_class_name("pointer").click()
    time.sleep(timesleep)
    chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
    
    
    
    chapter_content = ele.find_element_by_tag_name("ul")
    
    
    chapter_clickables = ele.find_elements_by_tag_name("span")
    chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
    chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
    
    chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
      
    articles = OrderedDict()
    for artcl in chapter_articles_and_paragraphs:
        
        artcl[0].click()
        time.sleep(timesleep)
        
        article_title_element = driver.find_element_by_class_name("doc.relative")
        article_title_tag = article_title_element.find_element_by_class_name("center").text
        try:
            article_title_text = article_title_element.find_element_by_class_name("center.dc_srch_trgt").text
        except:
            article_title_text = ''
        if article_title_text:
            article_title = article_title_tag + ' - ' + article_title_text
        else:
            article_title = article_title_tag

        if len(artcl) == 1:
            article_body = driver.find_elements_by_tag_name("p")
            text = [x.text for x in article_body if x.text]
            article_text = " ".join(text)
            articles[article_title] = article_text
        elif len(artcl) > 1:
            paragraphs = OrderedDict()
            for i in range(1, len(artcl)):
                artcl[i].click()
                time.sleep(timesleep)
                text = driver.find_element_by_class_name("dc_srch_trgt").text
                paragraphs[i] = text
            articles[article_title] = paragraphs
        time.sleep(timesleep)

    chapters[chapter_title] = articles














































    
    
    