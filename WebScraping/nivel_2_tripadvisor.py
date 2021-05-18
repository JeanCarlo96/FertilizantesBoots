#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose #Permite editar un dato del árbol HTML
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['tripadvisor.co']

    start_urls = ['https://www.tripadvisor.co/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    #Tiempo que va a esperar entre cada requerimiento de Scrapy
    #2 segundos
    download_delay = 2

    #Rules: Reglas que dice al Spider a donde debe ir y a donde no ir
    rules = (
        Rule(
            LinkExtractor(
                #Links a permitir: En nuestro caso solo los que contenga /Hotel_Review- dentro
                allow=r'/Hotel_Review-'
            ), follow=True, callback = "parse_hotel" #Saber si se los quiere seguir o no
        ),
    )

    def quitarSimboloDolar(self, texto):
        nuevoTexto = texto.replace("$", "")
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r','').replace('\t', '')
        nuevoTexto = nuevoTexto.replace('US ', '')
        return nuevoTexto

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio',
                       './/div[@class="CEf5oHnZ"]/text()',
                       MapCompose(self.quitarSimboloDolar))
        item.add_xpath('descripcion',
                       '//div[contains(@class, "_2f_ruteS _1bona3Pu _2-hMril5")]/div[1]/text()',
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities', '//div[@class="_2rdvbNSg"]/text()')

        yield item.load_item()

    #scrapy runspider nivel_2_tripadvisor.py -o hoteles.csv