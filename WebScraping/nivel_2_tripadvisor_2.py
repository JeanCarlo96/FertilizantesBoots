#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose #Permite editar un dato del árbol HTML
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()

class TripAdvisor(CrawlSpider):
    name = "opinionestripadvisor"
    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 100 #Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    allowed_domains = ['tripadvisor.co']
    start_urls = ['https://www.tripadvisor.co/Hotels-g303845-zff12-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 3

    rules = (
        #Paginación de hoteles (h)
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'
            ), follow=True
        ),
        #Detalles de hoteles (v)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                #restrict_xpath: Especifica los lugares del árbol donde se deben buscar las URLs
                restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_filtered_out_hotels_sponsored_0"]//a[@data-clicksource="HotelName"]']
            ), follow=True,
        ),
        #Paginación de opiniones dentro de un hotel (h)
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),
        #Detalle del perfil de usuario (v)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@id="component_14"]//a[contains(@class, "ui_header")]']
            ), follow=True, callback='parse_opinion'
        ),
    )

    def obtenerCalificacion(self, texto):
        #ui_bubble_rating bubble_50
        calificacion = texto.split("_")[-1]
        calificacion = list(calificacion)
        return  calificacion[0]

    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_xpath('titulo', './/div[@class="_3IEJ3tAK _2K4zZcBv"]/text()')
            item.add_xpath('calificacion', './/div[@class="_1VhUEi8g _2K4zZcBv"]/span/@class', MapCompose(self.obtenerCalificacion))
            item.add_xpath('contenido', './/q/text()')
            item.add_value('autor', autor)

            yield item.load_item()

#scrapy runspider nivel_2_tripadvisor_2.py -o trip_2.json