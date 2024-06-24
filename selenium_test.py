# Note to self: ko iščeš po css selectorju moreš "extractat" besedilo tako da daš <spremenljivka>.text
# ker iščeš tag "a" s classom "url-title-d" daš piko, če pa bi iskal tag z ID bi dal "#"

import time
import os
import filecmp
from tqdm import tqdm
import pandas as pd
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import data_module

### GLOBALNE SPREMENLJIVKE ###
ls_cene = []
ls_mesta = []
ls_kvadrature = []
ls_leto = []
ls_stevilo_sob = []
ls_url = []

### FUNKCIJE ###
def get_data():
    cene = driver.find_elements(By.CSS_SELECTOR, "div.property-details h6")
    for c in cene:
        ls_cene.append(c.text)
        
    # Najdem mesto
    mesta = driver.find_elements(By.CSS_SELECTOR, "a.url-title-d h2") 
    for m in mesta:
        ls_mesta.append(m.text)

    # Locate all <ul> elements with the itemprop attribute 'disambiguatingDescription' - v teh elementih se nahaja kvadratura, leto ...
    ul_elements = driver.find_elements(By.CSS_SELECTOR, 'ul[itemprop="disambiguatingDescription"]')

    # Iterate through each <ul> element to find the text in the <li> element
    for ul_element in ul_elements:
        # Najdem kvadraturo in leto glede na pozicijo v <ul> elementu
        kvadratura = ul_element.find_elements(By.TAG_NAME, 'li')[0]
        leto = ul_element.find_elements(By.TAG_NAME, 'li')[1]

        ls_kvadrature.append(kvadratura.text)
        ls_leto.append(leto.text)
    
    # URL oglasa
    urls = driver.find_elements(By.CSS_SELECTOR, "a.url-title-d") 
    for url in urls:
        ls_url.append(url.get_attribute("href"))
    
    #število sob
    st_sob = driver.find_elements(By.CSS_SELECTOR, "span.tipi")
    for st in st_sob:
        ls_stevilo_sob.append(st.text)

### ZAČETEK PROGRAMA ###

link = "https://www.nepremicnine.net/oglasi-prodaja/juzna-primorska/stanovanje/"

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Firefox(options=options)
driver.get(link)

num_pages = int((driver.find_element(By.CSS_SELECTOR, "ul[data-pages]")).get_attribute("data-pages"))
prisotnost = True

driver.close()
time.sleep(3)

print(f"Število strani nepremičnin: {num_pages}")

for i in tqdm(range(0,num_pages), desc="Scrapam strani"):
    driver = webdriver.Firefox(options=options)
    driver.get(link)
    get_data()
    
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a.next")
        link= next_btn.get_attribute("href")
    except NoSuchElementException:
        print("\nPrišel sem do konca seznama nepremičnin.")
        break
    driver.close()
    time.sleep(2)  

# ustvarim dataFrame
df = pd.DataFrame(list(zip(ls_mesta, ls_cene, ls_kvadrature, ls_stevilo_sob, ls_leto, ls_url)))
df.columns = ["Mesto", "Cena", "Kvadratura", "Število sob", "Leto", "Link"]
df.to_excel("nepremicnine_obala.xlsx", index=False)

# def replace_and_check(string):
#     split = string.split(" ")
#     split[0] = split[0].replace(".", "")
#     split[0] = split[0].replace(",", ".")
#     return float(split[0])

# df["Cena"] = df["Cena"].apply(replace_and_check)

# # Specifičen data frame za: KOPER, <350000€, 3,4,5 sobno
# spec_df = df[(df["Mesto"] == "KOPER") & (df["Cena"] < max_cena) & ((df["Število sob"] == "3-sobno") | (df["Število sob"] == "4-sobno") | (df["Število sob"] == "5 in večsobno"))]
# spec_df.to_excel("kp_nep.xlsx", index=False)

data_module.execute_replace(df)
data_module.execute_comparison(df)

driver.quit()
print("Program je zaključil")