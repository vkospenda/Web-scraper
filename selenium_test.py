import time
from tqdm import tqdm
import pandas as pd
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

### GLOBALNE SPREMENLJIVKE ###
ls_cene = []
ls_mesta = []
ls_kvadrature = []
ls_leto = []

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

#file = "cene.txt"
link = "https://www.nepremicnine.net/oglasi-prodaja/juzna-primorska/stanovanje/"

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Firefox(options=options)
driver.get(link)


# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyButtonAccept")))

# poskus = 0
# while(poskus < 3):
#     try:
#         cookie = driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonAccept")
#     except:
#         poskus += 1
#         print("Napaka pri CookieBot")
#     else:
#         print("Našel CookieBot")
#         break

# action = ActionChains(driver)
# action.click(on_element=cookie)
# action.perform()

num_pages = int((driver.find_element(By.CSS_SELECTOR, "ul[data-pages]")).get_attribute("data-pages"))
#num_pages = 3 #samo test
#curr_page = 1
prisotnost = True

# print(f"Procesiram stran {curr_page}")
# get_data()

# curr_page += 1

# next_btn = driver.find_element(By.CSS_SELECTOR, "a.next")
# link = next_btn.get_attribute("href")

driver.close()
time.sleep(3)


# Note to self: ko iščeš po css selectorju moreš "extractat" besedilo tako da daš <spremenljivka>.text
# ker iščeš tag "a" s classom "url-title-d" daš piko, če pa bi iskal tag z ID bi dal "#"


for i in tqdm(range(0,num_pages+1), desc="Scrapam strani"):
    #print(f"Procesiram stran {i}")
    driver = webdriver.Firefox(options=options)
    driver.get(link)
    get_data()
    
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a.next")
        link= next_btn.get_attribute("href")
    except NoSuchElementException:
        break
    driver.close()
    #curr_page += 1
    time.sleep(5)
    
        

# ustvarim dataFrame
# df = pd.DataFrame(list(zip(ls_mesta, ls_cene, ls_kvadrature, ls_leto)))
# df.columns = ["Mesta", "Cene", "Kvadrature", "Leto"]
# df.to_excel("cenik.xlsx")
#print(df)

driver.quit()
print("Program je zaključil")

