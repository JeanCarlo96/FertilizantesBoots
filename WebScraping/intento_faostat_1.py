import requests
from lxml import html
#Encabezados: Pide información de como se hace el requerimiento
#Modificamos el valor del encabezado "user-agent" para evitar que detecte como Bot
encabezados = {
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

#Url semilla
url = "https://es.wikipedia.org/wiki/Fertilizante"

#Hacemos el requerimiento
respuesta = requests.get(url, headers=encabezados)

#Tranforma la cadena de texto del árbol HTML en un parseador
parser = html.fromstring(respuesta.text)

#Expresiones xpath
#Para extraer la palabra English
print(parser.xpath("//table//th/text()"))
titulos = parser.xpath("//table//th/text()")
for t in titulos:
    print(t.rstrip('\n'))
paises = parser.xpath("//table//a/text()")
for p in paises:
    print(p.rstrip('\n'))
toneladas = parser.xpath("//table//td/text()")
for t in toneladas:
    print(t.rstrip('\n'))






