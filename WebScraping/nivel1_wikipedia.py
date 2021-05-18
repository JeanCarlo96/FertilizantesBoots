import requests
from lxml import html
#Encabezados: Pide información de como se hace el requerimiento
#Modificamos el valor del encabezado "user-agent" para evitar que detecte como Bot
encabezados = {
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

#Url semilla
url = "https://www.wikipedia.org/"

#Hacemos el requerimiento
respuesta = requests.get(url, headers=encabezados)

#Tranforma la cadena de texto del árbol HTML en un parseador
parser = html.fromstring(respuesta.text)

#Obtener un elemento por id
ingles = parser.get_element_by_id("js-link-box-en")

#Impresión del elemento
print(ingles.text_content())

#Expresiones xpath
#Para extraer la palabra English
print(parser.xpath("//a[@id='js-link-box-en']/strong/text()"))

#Para extraer todos los idiomas
#Forma 1:
idiomas = parser.xpath("//a/strong/text()")
print("Idiomas: ", idiomas)

#Forma 2:
idiomas = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
print("Idiomas: ", idiomas)

#Recorrer eleento por elemento
for elem in idiomas:
    print(elem)

#Forma 3:
idiomas = parser.find_class('central-featured-lang')
for elem in idiomas:
    print(elem.text_content())

