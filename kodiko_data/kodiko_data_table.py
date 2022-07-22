import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy as np
import json


def main(hrefdata):
    
    listOfRows = []
    for k, v in hrefdata.items():
        
        # Iterate through each url
        url = v[0]
        driver.get(url)
        time.sleep(timesleep)
        
        # Try to click accept the conditions button
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn btn-success pull-right']"))).click()
        except:
            pass
        
        # Find the clickable elements inside body section and skip the whole issue if does not contain any info
        try:
            body = driver.find_element_by_xpath("//body/div[@id='app']/div[@id='wrapper']/div[@id='sidebar-wrapper']/div[@id='document_navigation']/ul/li/ul/li/ul[1]")
        except:
            continue # skip if we cannot find body content
        clickables = body.find_elements_by_tag_name("span")
        clickables = [x for x in clickables if "[-]" not in x.text]
        
        # Find identity of Issue (eg. "Π.Δ. 11/2022")
        identity_class = driver.find_element_by_css_selector("h1[class='center left-md']")
        identity = identity_class.text
        time.sleep(timesleep)
        
        # Get levels for each items as a tuple (eg. ("Κεφάλαιο", 0), (Άρθρο, 1))
        q = driver.find_element_by_xpath('//*[@id="document_navigation"]/ul/li/ul/li[2]')
        dynamic_list = []
        def get_items_level(el, i=0):
            children = el.find_elements_by_xpath("./ul/li[*]")  # get children
            if children:
                for child in children:
                    tmp = child.find_element_by_xpath("./div")
                    attr = tmp.get_attribute('data-name')
                    dynamic_list.append((attr, i))
                    get_items_level(child, i+1)
        get_items_level(q)
        
        # Assert the elements in body section are equal to the levels computed above
        assert len(clickables) == len(dynamic_list)
        
        # Iterate through each element, click it and get its details [key, level, title, content]
        for i in range(len(clickables)):
            clickables[i].click()
            time.sleep(timesleep)
            key, level = dynamic_list[i][0], dynamic_list[i][1]
        
            if "Παρ" in key:
                content = driver.find_element_by_class_name("dc_srch_trgt").text
                row = {"identity": identity, "key": key, "title": np.NaN, "content": content, "level": level}
            else:
                basic_el = driver.find_element_by_class_name("doc.relative")
                if i+1 < len(clickables): next_key = dynamic_list[i+1][0]
                if "Άρθρο" in key and "Παρ" not in next_key:
                    try:
                        title = basic_el.find_element_by_class_name("center.dc_srch_trgt").text
                    except:
                        title = np.NaN
                    try:
                        content = basic_el.find_element_by_xpath("./div[@class='dc_srch_trgt']").text
                    except:
                        content = np.NaN
                    row = {"identity": identity, "key": key, "title": title, "content": content, "level": level}
                else:
                    try:
                        title = basic_el.find_element_by_class_name("center.dc_srch_trgt").text
                    except:
                        title = np.NaN
                    try:
                        intro = basic_el.find_element_by_xpath("./div[@class='dc_srch_trgt']").text
                    except:
                        intro = np.NaN
        
                    if title and intro:
                        row = {"identity": identity, "key": key, "title": title, "content": intro, "level": level}
                    elif title:
                        row = {"identity": identity, "key": key, "title": title, "content": np.NaN, "level": level}
                    elif intro:
                        row = {"identity": identity, "key": key, "title": np.NaN, "content": intro, "level": level}
                    else:
                        row = {"identity": identity, "key": key, "title": np.NaN, "content": np.NaN, "level": level}
            listOfRows.append(row)
    return pd.DataFrame(listOfRows)


if __name__ == "__main__":
    start = time.time()
    timesleep = 0.6
    data = pd.DataFrame(columns=["id", "key", "title", "content", "level"])
    
    with open("kodiko_href.json", "r", encoding='utf-8') as s:
        hrefdata = json.load(s)
    
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

    # driver = webdriver.Firefox(options=options)
    
    # Testing subset of urls_dict
    step, counter = 5, 1
    for i in range(0, len(hrefdata), step):
        dummyhrefdata = {k: hrefdata[k] for k in list(hrefdata.keys())[i:i+step]}
        new_data = main(dummyhrefdata)
        print("So far {} urls have been processed".format(counter*step))
        counter+=1
        data = data.append(new_data, ignore_index=True)
        
        if (counter*step % 500) == 0:
            title = "final_kodiko_data.csv"
            data.to_csv(title, encoding="utf-8", index=False, mode="a")
            data = pd.DataFrame(columns=["id", "key", "title", "content", "level"])
    # data.to_csv("final_kodiko_data.csv", encoding="utf-8", index=False)




