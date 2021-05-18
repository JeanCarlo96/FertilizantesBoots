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
    contenido = Field()

class Review(Item):
    titulo = Field()
    calificacion = Field()

class Video(Item):
    titulo = Field()
    fecha_de_publicacion = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'

    #Definición del encabezado para que no detecte que somos Bot
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 25 #Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    allowed_domains = ['latam.ign.com']

    download_delay = 1

    start_urls = ['https://latam.ign.com/se/?q=avengers&order_by=-date&type=video']

    rules = (
        #Horizontalidad por tipo de información: Artículo, review y juegos
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        #Horizontalidad por paginación
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'
            ), follow=True
        ),
        #Una regla por cada tipo de contenido
        #Reviews
        Rule(
            LinkExtractor(
              allow=r'/review/'
            ), follow=True, callback='parse_review'
        ),
        #Videos
        Rule(
            LinkExtractor(
              allow=r'/video/'
            ), follow=True, callback='parse_video'
        ),
        #Artículos
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_news'
        ),
    )

    def quitarSimbolos (self, texto):
        nuevoTexto = texto.replace("$", "")
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r', '').replace('\t', '')
        nuevoTexto = nuevoTexto.replace('US ', '')
        return nuevoTexto

    def parse_news(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo', '//h1[@id="id_title"]/text()', MapCompose(self.quitarSimbolos))
        item.add_xpath('contenido', '//div[@id="id_text"]//*/text()', MapCompose(self.quitarSimbolos))

        yield item.load_item()

    def parse_review(self, response):
        item = ItemLoader(Review(), response)
        item.add_xpath('titulo', '//h1[@class="strong"]/text()', MapCompose(self.quitarSimbolos))
        item.add_xpath('calificacion', '//span[@class="side-wrapper side-wrapper hexagon-content"]/text()', MapCompose(self.quitarSimbolos))

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_xpath('titulo', '//h1[@id="id_title"]/text()', MapCompose(self.quitarSimbolos))
        item.add_xpath('fecha_de_publicacion', '//span[@class="publish-date"]/text()', MapCompose(self.quitarSimbolos))

        yield item.load_item()

#scrapy runspider nivel_2_ign.py -o ign.json