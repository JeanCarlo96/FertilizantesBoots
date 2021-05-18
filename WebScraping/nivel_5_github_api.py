import requests
import json

#Encabezados
headers = {
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

endpoint = "https://api.github.com/user/repos?page=1"

usuario = "JeanCarlo96"
password = "pl33nkmldr7wx"

#Requerimiento con autenticación
#respuesta en formato Json
respuesta = requests.get(endpoint, headers=headers, auth=(usuario, password))

#Impresión de los datos extraidos
#print(json.dumps(respuesta.json(), indent=4))
repositorios = respuesta.json()

for repositorio in repositorios:
    print("Nombre:", repositorio['name'])

