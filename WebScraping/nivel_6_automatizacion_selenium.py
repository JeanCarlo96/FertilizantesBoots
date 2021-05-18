import schedule
import time
from selenium import webdriver
#Librerías para obtener la fecha actual
from datetime import date
from datetime import datetime

start_urls = {
    "https://www.accuweather.com/es/ec/tulcan/122056/weather-forecast/122056",
    "https://www.accuweather.com/es/ec/ibarra/123095/weather-forecast/123095",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846"
}

#Toda el proceso de selenium dentro de una función
def extraer_datos():

    driver = webdriver.Chrome('./chromedriver.exe')

    for url in start_urls:
        driver.get(url)

        #Extracción de datos
        ciudad = driver.find_element_by_xpath('//h1').text.replace('\n', '').replace('\r', '').strip()
        temperatura = driver.find_element_by_xpath('/html/body/div/div[5]/div[1]/div[1]/div[2]/a/div[2]/div[1]/div/div[1]').text.replace('\n', '').replace('\r', '').replace('°', '').strip()
        hora = driver.find_element_by_xpath('//p[@class="cur-con-weather-card__subtitle"]').text.replace('\n', '').replace('\r', '').strip()

        #Fecha actual
        fecha = datetime.now()

        #Impresión de datos
        print(ciudad)
        print(temperatura)
        print(hora)

        print("Día: ", fecha.day)
        print("Mes: ", fecha.month)
        print("Año: ", fecha.year)
        print()

        #Guardado en archivo de datos
        f = open('./datos_clima_selenium.csv', 'a')
        f.write(ciudad + ', ' + temperatura + ', ' + hora + ', ' + str(fecha) +'\n')
        f.close()
    driver.close()

#Agendamiento
schedule.every(1).minute.do(extraer_datos)
#schedule.every(1).hour.do(extraer_datos())
#schedule.every(1).day.do(extraer_datos())

#Se ejecuta siempre y mira si tiene tareas pendientes
while True:
    schedule.run_pending()
    time.sleep(1)


