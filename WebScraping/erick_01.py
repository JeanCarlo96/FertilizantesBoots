import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class use_unittest(unittest.TestCase):
	def setUp(self):
		self.driver=webdriver.Chrome("chromedriver.exe")

	def test_cambiar_window(self):
		driver=self.driver
		driver.get("http://google.com.ec")
		time.sleep(3)
		driver.execute_script("window.open('');")
		time.sleep(3)
		driver.switch_to.window(driver.window_handles[1])
		driver.get("http://xvideos.com")
		time.sleep(3)
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(3)

if _name=='main_':
	unittest.main()