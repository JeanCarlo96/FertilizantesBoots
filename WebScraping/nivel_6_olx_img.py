import requests
from PIL import Image
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

#Instancia del driver de Google Chrome
driver = webdriver.Chrome('./chromedriver')

#Abrir la página donde quiero hacer scrapy
driver.get('https://www.olx.com.ec/items/q-abono')

for i in range(2):
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

#Ejecutar un script para hacer scroll total hacia arriba
driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
#Espero 5 segundos
sleep(5)
#Ejecutamos un script para hacer scroll total hacia abajo
driver.execute_script("window.scrollTo({top: 20000, behavior:'smooth'});")
#Esperamos otros 5 segundos
sleep(5)

#Encontrar todos los items
#Todos los aununcios en una lista
anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

#Contador para nombre de la imagen
i = 1

#Extracción de cada uno de los elementos de la lista
for anuncio in anuncios:
    try:
        precio = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
        #print(precio)
        titulo = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
        #print(descripcion)
        ubicacion_completa = anuncio.find_element_by_xpath('.//span[@data-aut-id="item-location"]').text
        ubicacion = ubicacion_completa.split(",")[-1]

        try:
            #Extraigo la url que contiene la imagen
            url = anuncio.find_element_by_xpath('.//img').get_attribute('src')
            #Descargamos la imagen en binario
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            #Convertimos a imágen
            imagen = Image.open(image_file).convert('RGB')
            #Guardar en la carpeta imágenes
            path = './Imagenes/' + str(i) + '.jpg'
            #Abrimos el archivo
            with open(path, 'wb') as f:
                imagen.save(f, "JPEG", quality=85)
        except:
            print("Error en Imagen")


        #Incremento del contador que es nombre de la imagen
        i += 1

    except:
        continue
