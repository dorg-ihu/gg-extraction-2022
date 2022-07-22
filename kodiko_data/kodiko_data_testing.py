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
latin_numbers = ['I','II','III','IV','V','VI','VII','VIII','IX','X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX']

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

def outterParts(driver, top_level, inner_body, parts):
    
    for ele, tl in zip(inner_body, top_level):
        ele, tl = inner_body[0], top_level[0]
        tl.click()
        time.sleep(2*timesleep)
        
        # Get PART title
        try:
            part_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
        except:
            part_title = 'ΜΕΡΟΣ ΧΧΧ'

        
        # part_clickables = ele.find_elements_by_tag_name("span")
        # part_clickables = [x for x in part_clickables if x.text != "[-]"]
        # part_clickables = [x for x in part_clickables if "ΜΕΡΟΣ" not in x.text]
        # part_clickables = [x for x in part_clickables if "Μέρος" not in x.text]
        # part_clickables = [x for x in part_clickables if "Υπο" not in x.text]
        
        part_clickables = ele.find_elements_by_tag_name("span")
        part_clickables = [x for x in part_clickables if x.text != "[-]"]
        part_clickables = [x for x in part_clickables if "ΜΕΡΟΣ" not in x.text]
        part_clickables = [x for x in part_clickables if "Μέρος" not in x.text]
        part_clickables = [x for x in part_clickables if "Υπο" not in x.text]
        #part_clickables = [x for x in part_clickables if y for y in latin_numbers not in x.text]
        
        #TODO make this adding patterns, instead of removing
        #ADD clicks
        part_clickables = [x for x in part_clickables if "Άρθρο" in x.text or "ΑΡΘΡΟ" in x.text]
        part_clickables = [x for x in part_clickables if "Κεφάλαιο" in x.text or "ΚΕΦΑΛΑΙΟ" in x.text]
        
        
        
        # Check if PART has CHAPTERS inside or straight ARTICLES
        chapters_exist = False
        for ele in part_clickables:
            if "ΚΕΦΑΛΑΙΟ" in ele.text or "Κεφάλαιο" in ele.text:
                chapters_exist = True
                break
        print("Chapters exist: ", chapters_exist)
        
        # The 2 cases from above
        if chapters_exist:
            part_chapters_articles_and_paragraphs = make_split_on_webelements(part_clickables, identifier=["ΚΕΦΑΛΑΙΟ", "Κεφάλαιο"])
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
            part_chapters_articles_and_paragraphs = make_split_on_webelements(part_clickables, identifier=["Άρθρο"])
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
        ele, tl = inner_body[0], top_level[0]
        tl.click()
        time.sleep(2*timesleep)
        try:
            chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
        except:
            chapter_title = 'Κεφάλαιο ΧΧΧ' #TODO
            
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




""" test urls """

# url = 'https://www.kodiko.gr/nomothesia/document/799698/p.d.-48-2022' # Με κεφάλαια - μεγάλο
# url = 'https://www.kodiko.gr/nomothesia/document/799977' # Μόνο άρθρα
# url = 'https://www.kodiko.gr/nomothesia/document/804141' # Με κεφάλαια μικρό
url = 'https://www.kodiko.gr/nomothesia/document/309270' # Με κεφάλαια και Άρθρα με (α)
#url = 'https://www.kodiko.gr/nomothesia/document/665553' # Με Μέρη και κεφαλαια με αρθρα ή απευθειας αρθρα
#url = 'https://www.kodiko.gr/nomothesia/document/400403' # χωρις σωμα
# url = 'https://www.kodiko.gr/nomothesia/document/772315' # με υποκεφαλαια

# our 19 urls
url = "https://www.kodiko.gr/nomothesia/document/665553" # Δικαιοσύνης
url = "https://www.kodiko.gr/nomothesia/document/772315" # Ανάπτυξης και επενδύσεων
url = "https://www.kodiko.gr/nomothesia/document/305481" # Αγροτικής ανάπτυξης και τροφίμων
url = "https://www.kodiko.gr/nomothesia/document/674430" # Εξωτερικών και απόδημου ελληνισμου (Νόμος)
url = "https://www.kodiko.gr/nomothesia/document/348494" # Εργασίας και κοινωνικής ασφάλισης
url = "https://www.kodiko.gr/nomothesia/document/349078" # Εσωτερικών
url = "" # κλιματικής κρίσης και πολιτικής προστασίας
url = "https://www.kodiko.gr/nomothesia/document/662932" # μεταναστευσης και ασυλου
url = "https://www.kodiko.gr/nomothesia/document/349957" # ναυτιλιας και νησιωτικης πολιτικης
url = "https://www.kodiko.gr/nomothesia/document/331332" # οικονομικων
url = "https://www.kodiko.gr/nomothesia/document/349509" # παιδειας
url = "https://www.kodiko.gr/nomothesia/document/348123" # περιβαλλοντος και ενεργειας
url = "https://www.kodiko.gr/nomothesia/document/350677" # πολιτισμου και αθλητισμου
url = "https://www.kodiko.gr/nomothesia/document/532386" # προστασιας του πολιτη
url = "https://www.kodiko.gr/nomothesia/document/616684" # ψηφιακης διακυβερνησης
url = "https://www.kodiko.gr/nomothesia/document/308558" # τουρισμου
url = "https://www.kodiko.gr/nomothesia/document/309270" # υγειας
url = "https://www.kodiko.gr/nomothesia/document/309441" # υποδομων και μεταφορων





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
# if not inner_body: isEmpty = True


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

    


























# for ele in inner_body:
#     if "ΚΕΦΑΛΑΙΟ" or "Κεφάλαιο" in ele.text:
#         chapters_exist = True
#         break
    
        

# if chapters_exist:
#     chapters = OrderedDict()
#     top_level = driver.find_elements_by_xpath("//span[contains(text(),'Κεφάλαιο')] | //span[contains(text(),'ΚΕΦΑΛΑΙΟ')]")
#     assert len(top_level) == len(inner_body)
#     for ele, tl in zip(inner_body, top_level):

#         tl.click()
#         time.sleep(1)
#         try:
#             chapter_title = driver.find_element_by_class_name("doc.relative").text.replace("\n", " - ")
#         except:
#             chapter_title = 'Κεφάλαιο ΧΧΧ'
            
#         chapter_clickables = ele.find_elements_by_tag_name("span")
        
#         # for click in chapter_clickables:
#         #     if click.text == "[+]":
#         #         click.click()
        
#         chapter_clickables = [x for x in chapter_clickables if x.text != "[-]"]
#         chapter_clickables = [x for x in chapter_clickables if "ΚΕΦΑΛΑΙΟ" not in x.text]
#         chapter_clickables = [x for x in chapter_clickables if "Κεφάλαιο" not in x.text]
        
#         time.sleep(1)
        
#         chapter_articles_and_paragraphs = make_split_on_webelements(chapter_clickables)
        
#         articles = OrderedDict()
#         for artcl in chapter_articles_and_paragraphs:
            
            
#             artcl[0].click()
#             time.sleep(0.4)
            
#             article_title_element = driver.find_element_by_class_name("doc.relative")
            
#             try:
#                 article_title_tag = article_title_element.find_element_by_class_name("center").text
#             except:
#                 time.sleep(2)
#                 try:
#                     article_title_tag = article_title_element.find_element_by_class_name("center").text
#                 except Exception as e:
#                     print(e)
#                     article_title_tag = ''
            
#             try:
#                 article_title_text = article_title_element.find_element_by_class_name("center.dc_srch_trgt").text
#             except:
#                 article_title_text = ''
            
#             if article_title_text:
#                 article_title = article_title_tag + ' - ' + article_title_text
#             else:
#                 article_title = article_title_tag

            
#             if len(artcl) == 1:
#                 article_body = driver.find_elements_by_tag_name("p")
#                 text = [x.text for x in article_body if x.text]
#                 article_text = " ".join(text)
#                 articles[article_title] = article_text
#             elif len(artcl) > 1:
#                 paragraphs = OrderedDict()
#                 for i in range(1, len(artcl)):
#                     artcl[i].click()
#                     time.sleep(0.3)
#                     text = driver.find_element_by_class_name("dc_srch_trgt").text
#                     paragraphs[i] = text
#                 articles[article_title] = paragraphs

#         chapters[chapter_title] = articles

# document["body"] = chapters

