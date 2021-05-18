#Librería para hacer los requerimientos
import requests
from bs4 import BeautifulSoup

#Encabezados: Pide información de como se hace el requerimiento
#Modificamos el valor del encabezado "user-agent" para evitar que detecte como Bot
headers = {
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

#Url semilla
url = "https://es.stackoverflow.com/questions"

#Hacemos los requerimientos
respuesta = requests.get(url, headers = headers)

soup = BeautifulSoup(respuesta.text)

#Obtenemos toda la estructura que contiene el listado de preguntas de StackOverFlow
contenedor_de_preguntas = soup.find(id="questions")

#Me aseguro que el tag del cual saco los elementos sea div y con la clase definida
lista_de_preguntas = contenedor_de_preguntas.find_all('div', class_="question-summary")

#Iterando la lista de preguntas
num = 1
for pregunta in lista_de_preguntas:
    #texto_pregunta = pregunta.find('h3').text
    #descripcion_pregunta = pregunta.find(class_='excerpt').text
    elemento_texto_pregunta = pregunta.find('h3')
    texto_pregunta = elemento_texto_pregunta.text

    #Le decimos que busque en los primos un div
    descripcion_pregunta = elemento_texto_pregunta.find_next_sibling('div').text

    descripcion_pregunta = descripcion_pregunta.replace('\n','').replace('\r', '').strip()
    print("#", num, ": ", texto_pregunta)
    print(descripcion_pregunta)
    print()
    num += 1