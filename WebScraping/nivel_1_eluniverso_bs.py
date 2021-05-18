#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):
    titular = Field()
    descripcion = Field()

class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ["https://www.eluniverso.com/deportes"]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        contenedor_noticias = soup.find_all('div', class_= 'view-content')
        for contenedor in contenedor_noticias:
            #recursive false: Para que solo busque en los hijos directos
            noticias = contenedor.find_all('div', class_='posts', recursive = False)
            for noticia in noticias:
                item = ItemLoader(Noticia(), response.body)

                titular = noticia.find('h2').text
                descripcion = noticia.find('p')
                if (descripcion != None):
                    descripcion = descripcion.text
                else:
                    descripcion = 'N/A'

                item.add_value('titular', titular)
                item.add_value('descripcion', descripcion)

                yield item.load_item()