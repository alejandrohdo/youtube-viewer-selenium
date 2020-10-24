from selenium import webdriver
from time import sleep

class Google:

 def __init__(self,username,password):
  PATH_CHROMEDRIVER = '/home/alejandro/Downloads/chromedriver_linux64-2/chromedriver'
  self.driver=webdriver.Chrome(PATH_CHROMEDRIVER)
  self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')
  sleep(3)
  self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
  self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
  self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
  sleep(3)
  self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
  self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
  sleep(2)
  self.driver.get('https://youtube.com')
  sleep(50)
  self.driver.close()

username='iisotecperu@gmail.com'
password='Iisotec2020xxxx'
mylike= Google(username,password)