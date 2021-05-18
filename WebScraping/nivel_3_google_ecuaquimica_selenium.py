import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

#Código JavaScript
scrollScript = """
    document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 20000)
"""

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

#Url Semilla Ecuaquimica Matriz
driver.get("https://www.google.com/maps/place/Ecuaquimica.+Ecuatoriana+de+productos+quimicos/@-2.0663324,-79.9419465,17z/data=!4m14!1m6!3m5!1s0x902d0d98f6fb9909:0xd0973f7e6c24a78d!2sEcuaquimica.+Ecuatoriana+de+productos+quimicos!8m2!3d-2.0663378!4d-79.9397578!3m6!1s0x902d0d98f6fb9909:0xd0973f7e6c24a78d!8m2!3d-2.0663378!4d-79.9397578!9m1!1b1")

#Esperar un tiempo hasta que se cargue por que es pesada
sleep(random.uniform(4.0,5.0))

#Número de scrolins
SCROLLS = 0
while (SCROLLS != 3):
    #Ejecuta código de JavaScript
    driver.execute_script(scrollScript)
    #Espera de carga
    sleep(random.uniform(5.0, 6.0))
    SCROLLS += 1

reviews_agripac = driver.find_elements(By.XPATH, '//div[contains(@class, "section-review ripple-container")]')

for review in reviews_agripac:
    calificacion = review.find_element(By.XPATH, './/span[@class="section-review-stars"]').get_attribute('aria-label')
    comentario = review.find_element(By.XPATH, './/span[@class="section-review-text"]').text
    if(comentario == ""):
        comentario = "Ninguno"
    print(calificacion)
    print(comentario)
    print("")