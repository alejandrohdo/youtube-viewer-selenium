from selenium import webdriver
from time import sleep

class AuthGoogle:
  """Metodo alternativo de login en google, para el servicio youtube"""

    def __init__(self,username,password):
        self.PATH_CHROMEDRIVER = '/home/alejandro/Downloads/chromedriver_linux64-2/chromedriver'
        self.username = username
        self.password = password
        
    def login_google(self):
        driver=webdriver.Chrome(self.PATH_CHROMEDRIVER)
        driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')
        sleep(3)
        driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        driver.find_element_by_xpath('//input[@type="email"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(3)
        driver.find_element_by_xpath('//input[@type="password"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        sleep(2)
        driver.get('https://youtube.com')
        return driver
