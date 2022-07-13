import time
start = time.time()
#from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
from collections import OrderedDict


def login(driver, timesleep):
    
    email = "christantonis.kons@gmail.com"
    password = 123456
    
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


def main(hrefdata, loginS, timesleep):
    
    # Instantiate the driver
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    
    # Login to the website if login=True - Default False
    if loginS:
        driver.get("https://www.kodiko.gr/")
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
        driver = login(driver, timesleep)
    
    documents = OrderedDict()
    
    for k, v in hrefdata.items():
        
        # Iterate through each url
        url = v[0]
        driver.get(url)
        
        # Check if Accept Conditions button exist and click if so
        try:
            WebDriverWait(driver, 5*timesleep).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
        except:
            pass
        
        # Instantiate the dictionary that will contain the individual info of each item
        document = OrderedDict()
        
        # Get 1) Issue Number/Date from Landing Page and Find "Κεφαλίδα" and store 2) Prerequisites 3) Title
        identifier = driver.find_element_by_css_selector("h1[class='center left-md']")
        IDENTITY = identifier.text
        time.sleep(3*timesleep)
        
        HEADER = driver.find_element_by_xpath("//span[contains(text(),'Κεφαλίδα')]")
        HEADER.click()
        time.sleep(3*timesleep)
        
        try:
            header_content = driver.find_element_by_class_name("dc_srch_trgt")
            #TITLE = header_content.find_elements_by_tag_name("p")[1].text
        except Exception as e:
            print("Header ", k)
            print(e)
            #TITLE = ''
        
        try:
            prereq = header_content.text
            prereq_idx = prereq.find("Έχοντας υπόψη")
            PREREQ = prereq[prereq_idx:].replace("\n", " ")
        except Exception as e:
            print("Prerequisites ", k)
            print(e)
            PREREQ = ''
        
        document["identity"] = IDENTITY
        #document["title"] = TITLE
        document["prereq"] = PREREQ
        
        # Click on "Σώμα"
        BODY = driver.find_element_by_xpath("//span[contains(text(),'Σώμα')]")
        BODY.click()
        time.sleep(timesleep)
        
        # Find the inner levels of "Σώμα" and tune the boolean variable "chapters_exist" respectively, 
        # This is done based on the existence of word "ΚΕΦΑΛΑΙΟ" on those levels. Default -False- 
        
        chapters_exist = False
        inner_body = driver.find_elements_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul/li")

        for ele in inner_body:
            if "ΚΕΦΑΛΑΙΟ" in ele.text or "Κεφάλαιο" in ele.text:
                chapters_exist = True
                break
        print("Chapters_exist ", chapters_exist)

        
        # If not chapters exist that means that inner levels only contain Άρθρα - Παράγραφοι
        # If chapters exist that means that we have Κεφάλαια - Άρθρα - Παράγραφοι
    
        if not chapters_exist:
            
            # Instantiate articles dictionary (since) chapters dont exist
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
            chapter_level = driver.find_elements_by_xpath("//span[contains(text(),'Κεφάλαιο')] | //span[contains(text(),'ΚΕΦΑΛΑΙΟ')]")
            assert len(chapter_level) == len(inner_body)
            
            for ele, cl in zip(inner_body, chapter_level):
                
                cl.click()
                time.sleep(3*timesleep)
                try:
                    chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
                except:
                    chapter_title = 'Κεφάλαιο ΧΧΧ'
                time.sleep(timesleep)

                chapter_clickables = ele.find_elements_by_tag_name("span")
                chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
                chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
                chapter_clickables = [x for x in chapter_clickables if "Κεφάλαιο" not in x.text]
                
                chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
                
                articles = OrderedDict()
                for artcl in chapter_articles_and_paragraphs:
                    
                    artcl[0].click()
                    time.sleep(timesleep)
                    
                    article_title_element = driver.find_element_by_class_name("doc.relative")
                    try:
                        article_title_tag = article_title_element.find_element_by_class_name("center").text
                    except:
                        article_title_tag = ''
                    try:
                        article_title_text = article_title_element.find_element_by_class_name("center.dc_srch_trgt").text
                    except:
                        article_title_text = ''
                    if article_title_text or article_title_tag:
                        article_title = (article_title_tag + ' - ' + article_title_text).strip()
                    else:
                        article_title = article_title_tag
                    
                    print(article_title)
                    
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
                            try:
                                text = driver.find_element_by_class_name("dc_srch_trgt").text
                            except:
                                print("Didn't find dc_srch_trgt element I replace with empty!", article_title)
                                text = ''
                            paragraphs[i] = text
                        articles[article_title] = paragraphs
                    else:
                        print("LOGIC ERROR")
                    time.sleep(timesleep)
            
                chapters[chapter_title] = articles
                
            document["body"] = chapters
    
    
        documents[k] = document
    driver.close()
    return documents


if __name__ == "__main__":
    timesleep = 0.6
    loginS = False
    with open("kodiko_href.json", "r", encoding='utf-8') as s:
        hrefdata = json.load(s)
    
    # Testing subset of urls_dict
    n = 10
    dummyhrefdata = {k: hrefdata[k] for k in list(hrefdata.keys())[:n]}

    documents = main(dummyhrefdata, loginS, timesleep)
    end = time.time()
    print("Execution time ", end-start)
    with open("kodiko_data_completed.json", 'w', encoding='utf-8') as fp:
        json.dump(documents, fp, ensure_ascii=False)
    


# chapters = driver.find_elements_by_xpath(".//span[contains(text(),'Κεφάλαιο')]")
# for ele in chapters:
#     ele.click()
#     # click_ele.location_once_scrolled_into_view
#     # click_ele.click()
#     time.sleep(2)
    

    
# with open("kodiko_data.json", "r", encoding='utf-8') as s:
#     data = json.load(s)


# for ele in inner_body:
    
#     chapter_body = ele.find_element_by_class_name("pointer").click()
#     time.sleep(timesleep)
#     chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
    
    
    
#     chapter_content = ele.find_element_by_tag_name("ul")
    
    
#     chapter_clickables = ele.find_elements_by_tag_name("span")
#     chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
#     chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
    
#     chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
      
#     articles = OrderedDict()
#     for artcl in chapter_articles_and_paragraphs:
        
#         artcl[0].click()
#         time.sleep(timesleep)
        
#         article_title_element = driver.find_element_by_class_name("doc.relative")
#         article_title_tag = article_title_element.find_element_by_class_name("center").text
#         try:
#             article_title_text = article_title_element.find_element_by_class_name("center.dc_srch_trgt").text
#         except:
#             article_title_text = ''
#         if article_title_text:
#             article_title = article_title_tag + ' - ' + article_title_text
#         else:
#             article_title = article_title_tag

#         if len(artcl) == 1:
#             article_body = driver.find_elements_by_tag_name("p")
#             text = [x.text for x in article_body if x.text]
#             article_text = " ".join(text)
#             articles[article_title] = article_text
#         elif len(artcl) > 1:
#             paragraphs = OrderedDict()
#             for i in range(1, len(artcl)):
#                 artcl[i].click()
#                 time.sleep(timesleep)
#                 text = driver.find_element_by_class_name("dc_srch_trgt").text
#                 paragraphs[i] = text
#             articles[article_title] = paragraphs
#         time.sleep(timesleep)

#     chapters[chapter_title] = articles


