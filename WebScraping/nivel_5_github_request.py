import requests
from lxml import html

#Encabezados
headers = {
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

#Página de login de Github
login_form_url = 'https://github.com/login'

#Manejo de sesión
session = requests.Session()

#Los requerimientos se hacen a travez de la sesión
login_form_res = session.get(login_form_url, headers=headers)

#Vamos a obtener el token válido del arbol html
parser = html.fromstring(login_form_res.text)
token_especial = parser.xpath('//input[@name="authenticity_token"]/@value')

#Url que se hace requerimiento POST
login_url = "https://github.com/session"

#Parametros que permiten que se inicie sesión
login_data = {
    "login": "JeanCarlo96",
    "password": "pl33nkmldr7wx",
    "commit": "Sing in",
    "authenticity_token": token_especial
}

#Realizamos el requerimiento POST
session.post(
    login_url,
    data= login_data,
    headers=headers
)

#Extracción de datos
#Url a la que accedo luego de loggearme
data_url = 'https://github.com/JeanCarlo96?tab=repositories'
respuesta = session.get(
    data_url,
    headers=headers
)

#Obtenemos el arbol HTML y lo parseamos
parser = html.fromstring(respuesta.text)
repositorios = parser.xpath('//h3[@class="wb-break-all"]/a/text()')
for repositorio in repositorios:
    print(repositorio)