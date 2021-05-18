#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Pregunta(Item):
    #Cuerpo de la clase: Definición de las propiedades que voy a extraer
    id = Field()
    pregunta = Field()
    #descripcion = Field()

#Clase core de scrapy: Va hacer los requerimientos y parseo
#Hereda de Spider por que es a una sola página
class StackOverFlowSpider(Spider):
    name = "MiPrimerSpider"
    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    #Url Semilla
    start_urls = ['https://es.stackoverflow.com/questions']

    #Función que va ha realizar el parseo
    def parse(self, response):
        #Como es solo una página web, Scrapy se encarga de automaticamente
        #hacer el requerimiento y obtener el html semilla

        #Utilizamos Selector para realizar el parseo
        #Este me sirve para hacer consltas a la clase
        sel = Selector(response)

        #Título de la página
        titulo_de_pagina = sel.xpath('//h1/text()').get()
        print(titulo_de_pagina)

        #Usamos xpath para encontrar la información
        preguntas = sel.xpath('//div[@id="questions"]//div[@class="question-summary"]')
        i = 0
        for pregunta in preguntas:
            #Cargar mis items
            #Primer parámetro: Instancia de la clase que tiene mi abstracción
            #Segundo parámetro: Elemento html donde está la información donde lleno los campos de mi clase
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('pregunta', './/h3/a/text()')
            #item.add_xpath('descripcion', './/div[@class="excerpt"]/text()')
            #Si quisieramos llenar con un valor
            item.add_value('id', i)
            i+= 1
            #Una especie de return: Manda a cargar en un archivo la información de mis items
            yield item.load_item()

#Para correr todo esto necesitamos de un comando por terminal
#scrapy runspider nivel_1_stackoverflow_scrapy.py -o archivo.csv
# scrapy runspider 3_stackoverflow.py -o resultados.csv -t csv

