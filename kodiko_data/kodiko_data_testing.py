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


# url = 'https://www.kodiko.gr/nomothesia/document/799698/p.d.-48-2022' # Με κεφάλαια - μεγάλο
# url = 'https://www.kodiko.gr/nomothesia/document/799977' # Μόνο άρθρα
url = 'https://www.kodiko.gr/nomothesia/document/804141' # Με κεφάλαια μικρό



options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)
#driver.maximize_window()

driver.get(url)


try:
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
except:
    pass
#time.sleep(timesleep)

document = OrderedDict()

identifier = driver.find_element_by_css_selector("h1[class='center left-md']")
IDENTITY = identifier.text
time.sleep(2)

HEADER = driver.find_element_by_xpath("//span[contains(text(),'Κεφαλίδα')]")
HEADER.click()
time.sleep(2)

try:
    header_content = driver.find_element_by_class_name("dc_srch_trgt")
    #TITLE = header_content.find_elements_by_tag_name("p")[1].text
except Exception as e:
    print(e)
    #TITLE = ''

try:
    prereq = header_content.text
    prereq_idx = prereq.find("Έχοντας υπόψη")
    PREREQ = prereq[prereq_idx:].replace("\n", " ")
except Exception as e:
    print("Prereq ", e)
    PREREQ = ''

document["identity"] = IDENTITY
#document["title"] = TITLE
document["prereq"] = PREREQ

# Click on "Σώμα"
BODY = driver.find_element_by_xpath("//span[contains(text(),'Σώμα')]")
BODY.click()
time.sleep(2)

inner_body = driver.find_elements_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul/li")


for ele in inner_body:
    if "ΚΕΦΑΛΑΙΟ" or "Κεφάλαιο" in ele.text:
        chapters_exist = True
        break



if chapters_exist:
    chapters = OrderedDict()
    top_level = driver.find_elements_by_xpath("//span[contains(text(),'Κεφάλαιο')] | //span[contains(text(),'ΚΕΦΑΛΑΙΟ')]")
    assert len(top_level) == len(inner_body)
    for ele, tl in zip(inner_body, top_level):

        tl.click()
        time.sleep(1)
        try:
            chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
        except:
            chapter_title = 'Κεφάλαιο ΧΧΧ'
            
        chapter_clickables = ele.find_elements_by_tag_name("span")
        
        # for click in chapter_clickables:
        #     if click.text == "[+]":
        #         click.click()
        
        chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
        chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
        chapter_clickables = [x for x in chapter_clickables if "Κεφάλαιο" not in x.text]
        
        time.sleep(1)
        
        chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
        
        articles = OrderedDict()
        for artcl in chapter_articles_and_paragraphs:
            
            artcl[0].click()
            time.sleep(0.3)
            
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
                    time.sleep(0.3)
                    text = driver.find_element_by_class_name("dc_srch_trgt").text
                    paragraphs[i] = text
                articles[article_title] = paragraphs

        chapters[chapter_title] = articles

document["body"] = chapters







