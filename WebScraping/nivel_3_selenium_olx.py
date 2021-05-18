import random
from time import sleep
from selenium import webdriver

#Instancia del driver de Google Chrome
driver = webdriver.Chrome('./chromedriver.exe')

#Abrir la página donde quiero hacer scrapy
driver.get('https://www.olx.com.ec/autos_c378')

#Damos clic en el valor de cargar más tres veces
boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')

for i in range(3):
    try:
        # Tiempo de espera antes de extraer la informaión
        boton.click()
        sleep(random.uniform(8.0, 10.0))
        boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
    except:
        break #Rompe las iteracciones

#Encontrar todos los items
#Todos los aununcios en una lista
autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

#Extracción de cada uno de los elementos de la lista
for auto in autos:
    precio = auto.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    print(precio)
    descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    print(descripcion)