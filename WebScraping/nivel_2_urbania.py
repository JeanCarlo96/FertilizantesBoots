#Importar librerías necesarias para trabajar con Scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose #Permite editar un dato del árbol HTML
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Departamento(Item):
    nombre = Field()
    direccion = Field()

class Urbaniape(CrawlSpider):
    name = "Departamento"

    # Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 25
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    allowed_domains = ['urbania.pe']

    download_delay = 1

    start_urls = [
        'https://urbania.pe/buscar/proyectos-departamentos?page=1',
        'https://urbania.pe/buscar/proyectos-departamentos?page=2',
        'https://urbania.pe/buscar/proyectos-departamentos?page=3',
        'https://urbania.pe/buscar/proyectos-departamentos?page=4',
        'https://urbania.pe/buscar/proyectos-departamentos?page=5',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto-'
            ), follow=True, callback="parse_depa"
        ),
    )

    def parse_depa(self, response):
        sel = Selector(response)
        item = ItemLoader(Departamento(), sel)

        item.add_xpath('nombre', '//h2[@class="info-title"]/text()')
        item.add_xpath('direccion', '//h2[@class="info-location"]/text()')

        yield item.load_item()

#scrapy runspider nivel_2_urbania.py -o departamentos.json