from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request

class Dummy(Item):
    titulo = Field()
    #titulo_iframe = Field()

class W3SCrawler(CrawlSpider):
    name = 'w3s'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['w3schools.com']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']

    download_delay = 2

    def parse(self, response):
        sel = Selector(response)
        titulo = sel.xpath('//*[@id="main"]/h1')

        item = ItemLoader(Dummy(), titulo)

        item.add_xpath('titulo', './/span/text()')

        #meta_data = {
        #    'titulo': titulo
        #}

        #iframe_url = sel.xpath('//div[@id="main"]//iframe[@width="99%"]/@src').get()

        #iframe_url = "https://www.w3schools.com/html/" + iframe_url

        yield item.load_item()

       # yield Request(iframe_url, callback=self.parse_iframe, meta= meta_data)

'''
    def parse_iframe(self, response):
        item = ItemLoader(Dummy(), response)
        item.add_xpath('titulo_iframe', '//div[@id="main"]//h1/span/text()')
        item.add_value('titulo', response.meta.get('titulo'))

        yield item.load_item()'''

#scrapy runspider nivel_4_html_embebido.py -o datos_embebidos.csv