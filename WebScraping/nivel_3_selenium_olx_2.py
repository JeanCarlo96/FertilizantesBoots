from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Instancia del driver de Google Chrome
driver = webdriver.Chrome('./chromedriver')

#Abrir la página donde quiero hacer scrapy
driver.get('https://www.olx.com.ec/')

for i in range(4):
    try:
        #Espera por eventos
        #Va a esperar hasta 10s que el XPATH se encuentre lleno
        boton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )

        boton.click()

        #Tengo que esperar que la información nueva se cargue
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]')
        )

    except  Exception as e:
        print(e)
        continue #Rompe las iteracciones

#Encontrar todos los items
#Todos los aununcios en una lista
anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

#Extracción de cada uno de los elementos de la lista
for anuncio in anuncios:
    try:
        precio = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
        print(precio)
        descripcion = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
        print(descripcion)
    except:
        continue
