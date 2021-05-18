from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Limpieza():

    def limpiar_texto(self, texto):
        texto_limpio = texto.replace("$", "").replace('\n', '').replace('\r', '').replace('\t', '').strip()
        return texto_limpio

limpiador = Limpieza()
texto = "$$ hola pinches perros"
print(limpiador.limpiar_texto(texto))

class Eventos():

    def __init__(self, driver):
        self.driver = driver

    def esperar_elemento(self, elemento):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, elemento))
        )