import requests
from bs4 import  BeautifulSoup

url_semilla = "https://file-examples.com/index.php/sample-documents-download/sample-doc-download/"

#Encabezados
headers = {
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

#Guardo el arbol HTML
resp = requests.get(url_semilla, headers=headers)
soup = BeautifulSoup(resp.text)

#Lista vacía para almacenar los urls de los archivos
urls = []

#Extraigo los links por la clase
descargas = soup.find_all('a',class_='download-button')
for descarga in descargas:
    #Extraigo el valor del atributo href
    urls.append(descarga["href"])

print(urls)

#Contador para nombre del archivo descargado
i = 1
for url in urls:
    #Permitir que si la url realiza una redirección se la permita
    r = requests.get(url, allow_redirects=True)
    #Extracción de la extención del archivo
    ext = url.split('.')[-1]
    #print(ext)
    #Nombre del archivo
    file_name = './Archivos/word-file' + str(i) + '.' + ext
    #ab -> modo escribir especial (word, pdf, excel, etc)
    output = open(file_name, 'ab')
    #Cargamos el contenido al archivo
    output.write(r.content)
    #Cerramos el archivo
    output.close()
    i += 1



