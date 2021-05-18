from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
"user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
)

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

url = 'http://google.com/recaptcha/api2/demo'
driver.get(url)

try:
    #Cambiar el contexto para ver lo del iframe
    driver.switch_to.frame(driver.find_element_by_xpath('//iframe'))

    captcha = driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-border"]')
    captcha.click()

    #Parar el código hasta que aplastemos enter
    input()

    #Regresamos al contexto anterior
    driver.switch_to.default_content()

    submit = driver.find_element_by_xpath('//input[@id="recaptcha-demo-submit"]')
    submit.click()

except Exception as e:
    print(e)

#Ya estoy en la sguiente página
contenido = driver.find_element_by_class_name('recaptcha-success')
print(contenido.text)