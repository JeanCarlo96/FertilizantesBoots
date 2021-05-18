from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess

class ExtractorClima(Spider):
    name = "Clima"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': True # Elimina los miles de logs que salen al ejecutar Scrapy en terminal
    }

    start_urls = {
        "https://www.accuweather.com/es/ec/tulcan/122056/weather-forecast/122056",
        "https://www.accuweather.com/es/ec/ibarra/123095/weather-forecast/123095",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846"
    }

    #Todas las urls pasan por la función por defecto parse
    def parse(self, response):
        ciudad = response.xpath('//h1/text()').get().replace('\n', '').replace('\r', '').strip()
        temperatura = response.xpath('/html/body/div/div[5]/div[1]/div[1]/div[2]/a/div[2]/div[1]/div/div[1]/text()').get().replace('\n', '').replace('\r', '').replace('°', '').strip()
        hora = response.xpath('//p[@class="cur-con-weather-card__subtitle"]/text()').get().replace('\n', '').replace('\r', '').strip()

        print(ciudad)
        print(temperatura)
        print(hora)
        print()

        #Guardamos en un archivo
        f = open("./datos_clima_scrapy.csv", "a")
        f.write(ciudad + ', ' + temperatura + ', ' + hora + '\n')
        f.close()

#Correr scrapy desde aqui
#process = CrawlerProcess()
#process.crawl(ExtractorClima)
#process.start()

#Programar la ejecución del script
runner = CrawlerRunner()
#Indico cual es el Spider que yo quiero ejecutar
task = LoopingCall(lambda: runner.crawl(ExtractorClima))
#Cada cuanto ejecuto la tarea en segundos
task.start(20)
reactor.run()

