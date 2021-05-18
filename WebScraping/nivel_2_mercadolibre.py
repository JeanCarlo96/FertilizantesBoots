#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose #Permite editar un dato del árbol HTML
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
    ubicacion = Field()

class MercadoLibreFsertilizantes(CrawlSpider):
    name = "mercadoLibre"
    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20 #Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    #Lista de dominios a los cuales se permite dirigirse
    allowed_domains = ['listado.mercadolibre.com.ec', 'articulo.mercadolibre.com.ec']

    start_urls = ['https://listado.mercadolibre.com.ec/fertilizantes-agricolas#D[A:fertilizantes%20agricolas]']

    download_delay = 1

    rules = (
        #Paginación
        Rule(
            LinkExtractor(
                allow=r'/_Desde_\d+'
            ), follow=True
        ),
        #Detalle de productos
        Rule(
            LinkExtractor(
                allow=r'/MEC-'
            ), follow=True, callback='parse_items'
        ),

    )

    def quitarSimbolos (self, texto):
        nuevoTexto = texto.replace("$", "")
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r', '').replace('\t', '')
        nuevoTexto = nuevoTexto.replace('US ', '')
        return nuevoTexto

    def parse_items(self, response):
        item = ItemLoader(Articulo(),response)
        item.add_xpath('titulo', '//h1/text()', MapCompose(self.quitarSimbolos))
        item.add_xpath('descripcion', '//div[@class="item-description__text"]/p/text()', MapCompose(self.quitarSimbolos))
        item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()', MapCompose(self.quitarSimbolos))
        item.add_xpath('ubicacion', '//p[@class="card-description text-light"]/strong/text()', MapCompose(self.quitarSimbolos))

        yield item.load_item()

    #scrapy runspider nivel_2_mercadolibre.py -o fertilizantes.csv