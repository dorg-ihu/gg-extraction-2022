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

def outterParts(driver, top_level, inner_body, parts):
    
    for ele, tl in zip(inner_body, top_level):
        
        tl.click()
        time.sleep(2*timesleep)
        
        # Get PART title
        try:
            part_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
        except:
            part_title = 'ΜΕΡΟΣ ΧΧΧ'

        part_clickables = ele.find_elements_by_tag_name("span")        
        part_clickables = [x for x in part_clickables if x.text != "[-]"]
        part_clickables = [x for x in part_clickables if "ΜΕΡΟΣ" not in x.text]
        part_clickables = [x for x in part_clickables if "Μέρος" not in x.text]
        
        # Check if PART has CHAPTERS inside or straight ARTICLES
        chapters_exist = False
        for ele in part_clickables:
            if "ΚΕΦΑΛΑΙΟ" in ele.text or "Κεφάλαιο" in ele.text:
                chapters_exist = True
                break
        
        # The 2 cases from above
        if chapters_exist:
            part_chapters_articles_and_paragraphs = make_split_on_webelements(part_clickables, identifier="ΚΕΦΑΛΑΙΟ") #TODO make it also apply for "Κεφάλαιο"
            chapters = OrderedDict()
            
            for chptr in part_chapters_articles_and_paragraphs:
                chptr[0].click()
                try:
                    chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
                except:
                    chapter_title = 'Κεφάλαιο ΧΧΧ'
                
                chapter_articles_and_paragraphs = make_split_on_webelements(chptr)
                articles = OrderedDict()
                for artcl in chapter_articles_and_paragraphs[1:]:
                    
                    artcl[0].click()
                    time.sleep(2*timesleep)
                    
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
                    time.sleep(timesleep)
            
                chapters[chapter_title] = articles
                parts[part_title] = chapters
        else:
            part_chapters_articles_and_paragraphs = make_split_on_webelements(part_clickables, identifier="Άρθρο")
            articles = OrderedDict()
            for artcl in part_chapters_articles_and_paragraphs:
                
                artcl[0].click()
                time.sleep(2*timesleep)
                
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
            parts[part_title] = articles
    return parts

def outterChapters(driver, top_level, inner_body, chapters):
    
    for ele, tl in zip(inner_body, top_level):
        tl.click()
        time.sleep(2*timesleep)
        try:
            chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
        except:
            chapter_title = 'Κεφάλαιο ΧΧΧ'
            
        chapter_clickables = ele.find_elements_by_tag_name("span")
        chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
        chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
        chapter_clickables = [x for x in chapter_clickables if "Κεφάλαιο" not in x.text]
        time.sleep(timesleep)
        
        chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
        
        articles = OrderedDict()
        for artcl in chapter_articles_and_paragraphs:
            
            artcl[0].click()
            time.sleep(2*timesleep)
            
            article_title_element = driver.find_element_by_class_name("doc.relative")
            try:
                article_title_tag = article_title_element.find_element_by_class_name("center").text
            except:
                time.sleep(5*timesleep)
                try:
                    article_title_tag = article_title_element.find_element_by_class_name("center").text
                except Exception as e:
                    print(e)
                    article_title_tag = ''
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

        chapters[chapter_title] = articles
    return chapters

def outterArticles(driver, inner_body, articles):
    
    for ele in inner_body:
        article_clickables = ele.find_elements_by_tag_name("span")
        article_clickables[0].click()
        time.sleep(2*timesleep)
        
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
    return articles

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
            WebDriverWait(driver, 3*timesleep).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
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
        except Exception as e:
            print(e, "Header ", k)
        try:
            prereq = header_content.text
            prereq_idx = prereq.find("Έχοντας υπόψη")
            PREREQ = prereq[prereq_idx:].replace("\n", " ")
        except Exception as e:
            print(e, "Prerequisites ", k)
            PREREQ = ''
        
        document["identity"] = IDENTITY
        document["prereq"] = PREREQ
        
        # Click on "Σώμα"
        BODY = driver.find_element_by_xpath("//span[contains(text(),'Σώμα')]")
        BODY.click()
        time.sleep(timesleep)
        
        # Find the inner levels of "Σώμα" and tune the boolean variable "chapters_exist" respectively, 
        # This is done based on the existence of word "ΚΕΦΑΛΑΙΟ" on those levels. Default -False- 
        inner_body = driver.find_elements_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul/li")
        
        # If not data inside inner_body skip the current Issue
        if not inner_body:
            continue
        
        # Check which of the following levels exist in this Issue
        levels = []
        for ele in inner_body:
            structure = ele.text
            if "ΜΕΡΟΣ" in structure or "Μέρος" in structure:
                if "ΜΕΡΟΣ" not in levels: levels.append("ΜΕΡΟΣ")
            if "ΚΕΦΑΛΑΙΟ" in structure or "Κεφάλαιο" in structure:
                if "ΚΕΦΑΛΑΙΟ" not in levels: levels.append("ΚΕΦΑΛΑΙΟ")
            if "ΑΡΘΡΟ" in structure or "Άρθρο" in structure:
                if "ΑΡΘΡΟ" not in levels: levels.append("ΑΡΘΡΟ")
            if "ΠΑΡ" in structure or "Παρ" in structure:
                if "ΠΑΡΑΓΡΑΦΟΣ" not in levels: levels.append("ΠΑΡΑΓΡΑΦΟΣ")
        
        if "ΜΕΡΟΣ" in levels:
            parts = OrderedDict()
            top_level = driver.find_elements_by_xpath("//span[contains(text(),'ΜΕΡΟΣ')] | //span[contains(text(),'Μέρος')]")
            assert len(top_level) == len(inner_body)
            parts = outterParts(driver, top_level, inner_body, parts)
            document["body"] = parts
        elif "ΚΕΦΑΛΑΙΟ" in levels:
            chapters = OrderedDict()
            top_level = driver.find_elements_by_xpath("//span[contains(text(),'Κεφάλαιο')] | //span[contains(text(),'ΚΕΦΑΛΑΙΟ')]")
            assert len(top_level) == len(inner_body)
            chapters = outterChapters(driver, top_level, inner_body, chapters)
            document["body"] = chapters
        elif "ΑΡΘΡΟ" in levels:
            articles = OrderedDict()
            articles = outterArticles(driver, inner_body, articles)
            document["body"] = articles
        
        documents[k] = document
    driver.close()
    return documents


if __name__ == "__main__":
    timesleep = 0.6
    loginS = False
    with open("kodiko_href.json", "r", encoding='utf-8') as s:
        hrefdata = json.load(s)
    
    # Testing subset of urls_dict
    n = 20
    dummyhrefdata = {k: hrefdata[k] for k in list(hrefdata.keys())[:n]}

    documents = main(dummyhrefdata, loginS, timesleep)
    end = time.time()
    print("Execution time ", end-start)
    with open("kodiko_data_completed.json", 'w', encoding='utf-8') as fp:
        json.dump(documents, fp, ensure_ascii=False)
    





