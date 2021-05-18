from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
)

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

#Url semilla
driver.get('https://listado.mercadolibre.com.ec/fertilizantes-agricolas#D[A:fertilizantes%20agricolas]')

while True:
    #Extraer el listado de productos
    links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element ui-search-link"]')
    links_de_la_pagina = []
    print("número de links: ", len(links_productos))
    for tag_a in links_productos:
        #Para extraer la información del atributo href
        print(tag_a.get_attribute("href"))
        links_de_la_pagina.append(tag_a.get_attribute("href"))

    for link in links_de_la_pagina:
        try:
            #Hace que el navegador se dirija a una nueva URL
            driver.get(link)
            titulo = driver.find_element_by_xpath('//h1').text
            precio = driver.find_element(By.XPATH, '//span[@class="price-tag-fraction"]').text
            print(precio)
            print(titulo)
            #Regreso de página
            driver.back()
        except Exception as e:
            driver.back()
            print(e)

    print("Acabó con los links de la primera página")
    #Paginación
    try:
        boton_siguiente = driver.find_element(By.XPATH, '//li[@class="andes-pagination__button andes-pagination__button--next"]/a').get_attribute("href")
        #boton_siguiente.click()
        driver.get(boton_siguiente)
        print("Entro a boton siguiente")
    except:
        #Se va a romper el bucle cuando el boton siguiente ya no existe
        print("Error")
        break








