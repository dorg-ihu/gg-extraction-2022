import time
#start = time.time()
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#import json
from collections import OrderedDict

timesleep = 0.4

def find_paragraphs(driver, iterlist):
    paragraphs = OrderedDict()
    for i in range(1, len(iterlist)):
        iterlist[i].click()
        time.sleep(timesleep)
        text = driver.find_element_by_class_name("dc_srch_trgt").text
        paragraphs[i] = text
    return paragraphs

def find_article_title(driver):
    article_title_element = driver.find_element_by_class_name("doc.relative")
    try:
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
    return article_title

def make_split_on_webelements(thelist, identifier='Άρθρο'):
    """
    list of webelements
    """
    if len(thelist) == 0:
        return []
    r0, r1 = [], []
    for s in thelist:
        if identifier in s.text:
        #if any(idnt in s.text for idnt in identifier):
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

#TODO add "https://www.kodiko.gr/nomothesia/document/349509"
# url = "https://www.kodiko.gr/nomothesia/document/349509"

documents = OrderedDict()
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)

for url in urls:
    #url = urls[2]
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
    
    first_levels = driver.find_elements_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul/li")
    
    content = OrderedDict()
    for idx, ele in enumerate(first_levels):
        
        outer_level = ele.find_element_by_tag_name("span")
        
        if "Άρθρο" in outer_level.text:
            clickables = ele.find_elements_by_tag_name("span")
            clickables = [x for x in clickables if "[-]" not in x.text]
            clickables[0].click()
            article_title = find_article_title(driver)
            if len(clickables) == 1:
                article_body = driver.find_elements_by_tag_name("p")
                text = [x.text for x in article_body if x.text]
                article_text = " ".join(text)
                article = article_text
            else:
                paragraphs = find_paragraphs(driver, clickables)
                article = paragraphs
            content[article_title] = article
            continue
        else:
            inner_content = OrderedDict()
            clickables = ele.find_elements_by_tag_name("span")[1:]
            clickables = [x for x in clickables if "[-]" not in x.text]
            inner_level = [x for x in clickables if "Άρθρο" in x.text or "Παρ" in x.text]
            intermediate_level = [x for x in clickables if x not in inner_level] # TODO exclude possible level that is unnecessary
            
            # Get outer title
            outer_level.click()
            time.sleep(timesleep)
            outer_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
            print(outer_title)
            if intermediate_level:
                # Get clicks
                idx = [clickables.index(x) for x in intermediate_level]
                idx.append(len(clickables))
                intermediate_clicks = []
                for i in range(len(intermediate_level)):
                    intermediate_clicks.append(clickables[idx[i]:idx[i+1]])
                    
                for icl in intermediate_clicks:
                    icl[0].click()
                    inner_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
                    
                    articles_and_paragraphs = make_split_on_webelements(icl[1:])
                    articles = OrderedDict()
                    for artcl in articles_and_paragraphs:
                        artcl[0].click()
                        
                        # Article title
                        article_title = find_article_title(driver)
                        if len(artcl) == 1:
                            article_body = driver.find_elements_by_tag_name("p")
                            text = [x.text for x in article_body if x.text]
                            article_text = " ".join(text)
                            articles[article_title] = article_text
                        else:
                            paragraphs = find_paragraphs(driver, artcl)
                            articles[article_title] = paragraphs
                    inner_content[inner_title] = articles 
            else:
                articles_and_paragraphs = make_split_on_webelements(inner_level)
                for artcl in articles_and_paragraphs:
                    artcl[0].click()
                    time.sleep(timesleep)
                    # Article title
                    article_title = find_article_title(driver)
                    if len(artcl) == 1:
                        article_body = driver.find_elements_by_tag_name("p")
                        text = [x.text for x in article_body if x.text]
                        article_text = " ".join(text)
                        inner_content[article_title] = article_text
                    else:
                        paragraphs = find_paragraphs(driver, artcl)
                        inner_content[article_title] = paragraphs
        content[outer_title] = inner_content  
    document["content"] = content
    documents[url] = document














