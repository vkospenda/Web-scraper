from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

file = "cene.txt"

driver = webdriver.Firefox()
driver.get("https://www.nepremicnine.net/oglasi-prodaja/juzna-primorska/stanovanje/")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyButtonAccept")))

poskus = 0
while(poskus < 3):
    try:
        cookie = driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonAccept")
    except:
        poskus += 1
        print("Napaka pri CookieBot")
    else:
        print("Našel CookieBot")
        break

action = ActionChains(driver)
action.click(on_element=cookie)
action.perform()

# samo cene
cene = driver.find_elements(By.CSS_SELECTOR, "meta[itemprop='price']")
with open(file, "a") as f:
    for i in cene:
        #print(i.get_attribute("content"))
        f.write(i.get_attribute("content") + "\n")

# TODO: 1. poleg cene tudi enota (ni vedno €, je lahko tudi €/m2)
# TODO: 2. Naredit Git Repositorij
driver.quit()
print("Program je zaključil")