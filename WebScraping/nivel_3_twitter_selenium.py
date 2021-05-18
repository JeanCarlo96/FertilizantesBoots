import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

#Url Semilla Twitter
driver.get("https://twitter.com/login?lang=es")

user = "@jean_marchesini"
passwd = "doyoulovemejean"

#Espera hasta que cargue la página
input_user = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//main//input[@name="session[username_or_email]"]'))
)

input_passwd = driver.find_element(By.XPATH, '//main//input[@name="session[password]"]')

#Llenamos los campos
input_user.send_keys(user)
input_passwd.send_keys(passwd)

#Boton Iniciar Sesión
boton = driver.find_element(By.XPATH, '//main//div[@data-testid="LoginForm_Login_Button"]/div[@dir="auto"]')
boton.click()

#Espera de carga de tweets
#Extracción de los twitts
tweets = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//section//article//div[@dir="auto"]'))
)

for tweet in tweets:
    print(tweet.text)