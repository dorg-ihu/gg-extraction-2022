import time
#start = time.time()
#from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#import json
from collections import OrderedDict

timesleep = 0.4

def make_split_on_webelements(thelist, identifier=['Άρθρο']):
    """
    list of webelements
    """
    if len(thelist) == 0:
        return []
    r0, r1 = [], []
    for s in thelist:
        #if identifier in s.text:
        if any(idnt in s.text for idnt in identifier):
            if r1:
                r0.append(r1)
                r1 = []
        r1.append(s)
    return r0 + [r1]

""" urls """

urls = ["https://www.kodiko.gr/nomothesia/document/804306/p.d.-53-2022",
        "https://www.kodiko.gr/nomothesia/document/804375/p.d.-54-2022",
        "https://www.kodiko.gr/nomothesia/document/309270",
        "https://www.kodiko.gr/nomothesia/document/665553"]


# url = "https://www.kodiko.gr/nomothesia/document/804306/p.d.-53-2022"
# url = 'https://www.kodiko.gr/nomothesia/document/804375/p.d.-54-2022'
# url = 'https://www.kodiko.gr/nomothesia/document/799698/p.d.-48-2022' # Με κεφάλαια - μεγάλο
# url = 'https://www.kodiko.gr/nomothesia/document/799977' # Μόνο άρθρα
# url = 'https://www.kodiko.gr/nomothesia/document/804141' # Με κεφάλαια μικρό
# url = 'https://www.kodiko.gr/nomothesia/document/309270' # Με κεφάλαια και Άρθρα με (α)
# url = 'https://www.kodiko.gr/nomothesia/document/665553' # Με Μέρη και κεφαλαια με αρθρα ή απευθειας αρθρα
#url = 'https://www.kodiko.gr/nomothesia/document/400403' # χωρις σωμα
# url = 'https://www.kodiko.gr/nomothesia/document/772315'



documents = OrderedDict()
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)
#driver.maximize_window()

for url in urls:
    driver.get(url)
    
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
    except:
        pass
    
    document = OrderedDict()
    
    # Find Identity
    identity_class = driver.find_element_by_css_selector("h1[class='center left-md']")
    IDENTITY = identity_class.text
    document["identity"] = IDENTITY
    time.sleep(2)
    
    #click ΚΕΦΑΛΙΔΑ
    #header = driver.find_element_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li[1]")
    header = driver.find_element_by_xpath("//span[contains(text(),'Κεφαλίδα')]").click()
    time.sleep(2)
    
    try:
        header_content = driver.find_element_by_class_name("dc_srch_trgt")
        prereq = header_content.text
        prereq_idx = prereq.find("Έχοντας υπόψη")
        PREREQ = prereq[prereq_idx:].replace("\n", " ")
    except Exception as e:
        PREREQ = ''
        print(e)
        
    document["prereq"] = PREREQ
    
    
    #click ΣΩΜΑ
    body = driver.find_element_by_xpath("//span[contains(text(),'Σώμα')]").click()
    first_levels = driver.find_elements_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul/li")
    
    
    body = OrderedDict()
    for idx, ele in enumerate(first_levels):
        #ele = first_levels[0]
        #ele = first_levels[1]
        
        pointer_class = ele.find_element_by_class_name("pointer")
        data_name = pointer_class.get_attribute('data-name')
        
        if "Άρθρο" in data_name:
            clickables = ele.find_elements_by_tag_name("span")
            clickables[0].click()
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
            articles = OrderedDict()
            if len(clickables) == 1:
                article_body = driver.find_elements_by_tag_name("p")
                text = [x.text for x in article_body if x.text]
                article_text = " ".join(text)
                body[article_title] = article_text
            elif len(clickables) > 1:
                clickables = [x for x in clickables if x.text != "[-]"]
                paragraphs = OrderedDict()
                for i in range(1, len(clickables)):
                    clickables[i].click()
                    time.sleep(timesleep)
                    text = driver.find_element_by_class_name("dc_srch_trgt").text
                    paragraphs[i] = text
                body[article_title] = paragraphs
            #body["articles"] = articles
        else:
            
            ele.find_element_by_class_name("pointer").find_element_by_tag_name("span").click()
            
            try:
                first_level_title =  driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
            except:
                first_level_title = idx
            
    
            clickables = ele.find_elements_by_tag_name("span")    
            inner_clickables = [x for x in clickables if "Άρθρο" in x.text or "Παρ" in x.text]
            
            article_and_paragraphs = make_split_on_webelements(inner_clickables)
            articles = OrderedDict()
            
            for artcl in article_and_paragraphs:
                artcl[0].click()
                time.sleep(2*timesleep)
                
                # FIND ARTICLE TITLE
                article_title_element = driver.find_element_by_class_name("doc.relative")
                try:
                    time.sleep(0.4)
                    article_title_tag = article_title_element.find_element_by_class_name("center").text
                except:
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
                    #TODO check an uparxei eisagwgh sto arthro kai valto ws ksexwristo arthro
                    for i in range(1, len(artcl)):
                        artcl[i].click()
                        time.sleep(timesleep)
                        text = driver.find_element_by_class_name("dc_srch_trgt").text
                        paragraphs[i] = text
                    articles[article_title] = paragraphs
                body[first_level_title] = articles
    document["content"] = body
    documents[url] = document



































