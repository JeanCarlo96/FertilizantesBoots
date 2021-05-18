#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose #Permite editar un dato del árbol HTML
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Farmacia(Item):
    nombre = Field()
    precio = Field()

class CruzVerde(CrawlSpider):
    name = "Farmacias"

    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 25 #Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    allowed_domains = ['cruzverde.cl']

    download_delay = 1

    start_urls = ['https://www.cruzverde.cl/medicamentos/']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'start=\d+',
                #Me dice en que tags buscar urls
                tags=('a', 'button'),
                attrs=('href', 'data-url')

            ), follow=True, callback="parse_farmacia"
        ),
    )

    def quitarSimboloDolar(self, texto):
        nuevoTexto = texto.replace("$", "")
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r','').replace('\t', '').strip()
        nuevoTexto = nuevoTexto.replace('US ', '')
        return nuevoTexto

    def parse_farmacia(self, response):
        sel = Selector(response)
        productos = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for producto in productos:
            item = ItemLoader(Farmacia(), producto)

            item.add_xpath('nombre', './/div[@class="pdp-link"]/a/text()', MapCompose(self.quitarSimboloDolar))
            item.add_xpath('precio', './/span[@class="price-original"]/span/text()', MapCompose(self.quitarSimboloDolar))

            yield item.load_item()


#scrapy runspider nivel_2_cruz_verde.py -o farmacia.csv