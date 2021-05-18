import requests
import pandas as pd

#Cabeceros para no parece bot
headers = {
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'referer': 'https://www.udemy.com/courses/search/?src=ukw&q=python'
}

#Url que devuelve la información de los cursos de Udemy
url_api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p='
#url_api_2= 'https://www.udemy.com/api-2.0/search-courses/?p=2&q=python&src=ukw&skip_price=true'

#Diccionario que almacenará los datos de los cursos de udemy
cursos_totales = []

for i in range(1, 5):
    url_api_paginacion = url_api + '&p=' + str(i)

    #Requerimiento a la URL
    response = requests.get(url_api_paginacion, headers = headers)

    #Impresión de la respuesta
    #print(response.json())

    #Guardar la información
    #Se guarda como un diccionariio
    data = response.json()

    #Cramos una variable cursos, que extraiga solo esa información del json
    cursos = data['courses']

    #Imprimimos el título de los cursos
    for curso in cursos:
        print('titulo: ', curso['title'])
        print('número vistas: ', curso['num_reviews'])
        print('fecha: ', curso['last_update_date'])
        print()
        cursos_totales.append({
            "titulo": curso['title'],
            "num_vistas": curso['num_reviews'],
            "fecha": curso['last_update_date']
        })

df = pd.DataFrame(cursos_totales)

#Imprimir Tabla
print(df)

#Guardar como.csv la tabla
df.to_csv("cursos_udemy.csv")



    #Estructura en Pandas


