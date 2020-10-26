import json
import os
from selenium import webdriver
import selenium.webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from datetime import datetime
import time
from random import randint
from selenium.webdriver.common.keys import Keys 
from AuthGoogle import AuthGoogle


class YoutubeViewerRobot():
	"""Script que permite acceder a youtube y visualizar los videos por canal"""
	def __init__(self):
		self.driver = None

	def get_path_base_driver(self):
		"""path localtion driver"""
		full_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
		path, filename = os.path.split(full_path)
		return path

	def caculate_all_duration_time_play_list(self,list_time):
		# Calculando la duracion de reproduccion de todos los video en un play list
		list_minutes = []
		list_seconds = []
		for time in list_time:
			list_seconds.append(int(time.split(':')[0])*60)
			list_seconds.append(int(time.split(':')[1]))
		return sum(list_seconds)

	def extract_time_duration_play_list(self):
		try:
			print ('Extrayendo tiempos..')
			xpath = '//*[@id="playlist-items"]/a/div/div[2]//ytd-thumbnail-overlay-time-status-renderer//span'
			list_time = self.driver.find_elements_by_xpath(xpath)
			time.sleep(1)
			new_list_time  = []
				# list_time.append(time)
			for time_l in list_time:
				new_list_time.append(time_l.text)
			return self.caculate_all_duration_time_play_list(new_list_time)
			# print ('LIST TIME>', new_list_time)
		except Exception as e:
			print ('Error time play list>', e)

	def two_speed_play_video(self):
		'''Aumenta la velociadad de reproduccion a 2x'''
		try:
			xpath_config_video = '//*[@id="movie_player"]/div[25]//button[3]'
			#velocidad al final de xpath> div[8]=2, div[7]=1.75, div[6]=1.5,etc.
			self.driver.find_element_by_xpath(xpath_config_video).click() #click config
			time.sleep(1)
			xpath_playback_speed = "//div[contains(@class, 'ytp-popup ytp-settings-menu')]/div/div[1]/div[2]"
			# self.driver.find_element_by_xpath(xpath_playback_speed).click() #click velocidad reproduccion
			self.driver.find_element_by_xpath(xpath_playback_speed).send_keys(Keys.UP)
			self.driver.find_element_by_xpath(xpath_playback_speed).send_keys(Keys.ENTER)
			print ('PAso.................')
			time.sleep(1.5)
			xpath_playback_down = "//div[contains(@class, 'ytp-popup ytp-settings-menu')]/div/div/div[8]"
			# self.driver.find_element_by_xpath(xpath_playback_down).click()
			self.driver.find_element_by_xpath(xpath_playback_down).send_keys(Keys.DOWN + Keys.DOWN + Keys.DOWN + Keys.DOWN + Keys.ENTER)
			time.sleep(1)
			self.driver.find_element_by_xpath(xpath_config_video).send_keys(Keys.ESCAPE)
			return True
		except Exception as e:
			print ('Error xpath speed>', e)
		return False

	def click_stadistic(self):
		'''Realiza like y suscripcion al canal'''
		is_like_video = False
		try:
			is_xpath_text_like_video = "(//a//button[@id='button'])[5]/../../yt-icon-button[contains(@class,'style-default-active')]"
			is_xpath_text_not_like_video = "(//a//button[@id='button'])[5]/../../yt-icon-button[contains(@class,'style-text')]"
			time.sleep(1)
			is_like = self.driver.find_element_by_xpath(is_xpath_text_like_video)
			is_like_video = True
			print ('Ya se hizo like en el video se omite el click')
		except Exception as e:
			print ('Posiblemente aun no se hizo like', e)
			is_like_video = False
		try:
			if not is_like_video:
				xpath_like_video = "(//a//button[@id='button'])[5]/.."
				self.driver.find_element_by_xpath(xpath_like_video).click()
		except Exception as e:
			print ('Error al dar like video>', e)
			try:
				print('Posible alternativo..')
				xpath_like_video = "(//a//button[@id='button'])[8]/.."
				self.driver.find_element_by_xpath(xpath_like_video).click()
			except Exception as e:
				print('error 2do intento like video>', e)

	def init_chrome(self, is_auth=False, username=None, password=None):
		try:
			# PATH_FIREFOXDRIVER = '/home/alejandro/Downloads/chromedriver_linux64-2/chromedriver'
			PATH_FIREFOXDRIVER = '/home/alejandro/Downloads/geckodriver-v0.26.0-linux64/geckodriver'
			PATH_LOG = self.get_path_base_driver() +"/app/tweet/log/log_renovate_cookie_twitter.txt"
			options = Options()
			# options.add_argument("--headless")
			# options.add_argument("--mute-audio") # En firefox no funciona
			# options.add_argument('--no-sandbox')
			# options.add_argument('--disable-gpu')
			options.add_argument('--disable-gpu')
			options.add_argument('--disable-dev-shm-usage')
			# options.log.level = "trace"
			if is_auth:
				# profile.set_preference("media.volume_scale", "0.0")
				profile = webdriver.FirefoxProfile('/home/alejandro/.mozilla/firefox/1kj45idd.default')
				self.driver = webdriver.Firefox(
				    # capabilities=caps,
				    options=options, 
				    executable_path=PATH_FIREFOXDRIVER,
				    firefox_profile = profile
				    # log_path=self.get_path_base_driver()+'/log/twitter/drivefirefox.log'
			    )
			else:
				profile = webdriver.FirefoxProfile()
				profile.set_preference("media.volume_scale", "0.0")
				self.driver = webdriver.Firefox(
				    # capabilities=caps,
				    options=options, 
				    executable_path=PATH_FIREFOXDRIVER,
				    firefox_profile = profile
				)
		except Exception as e:
			print ('Erro al iniciar driver:', e)


	def get_open_browser(self, list_channels, count_viewers):
		"""Funcion que visita a twitter"""
		try:
			counter_for = 0 # solo para activar 2x por primeva vez
			activate_two_speed_play_video = False
			for channel in list_channels:
				print ('Visitando..', channel)
				self.driver.get(channel)
				try:
					xpath_view_video  = '//*[@id="play-all"]/ytd-button-renderer'
					self.driver.find_element_by_xpath(xpath_view_video).click()
					time.sleep(20)
					all_time_duration_play_list = self.extract_time_duration_play_list()
					# if counter_for ==0:
					print ('Aumentado velocidad de reproduccion')
					is_two_speed_play_video =  self.two_speed_play_video()
					if is_two_speed_play_video and all_time_duration_play_list>0:
						print ('Duracion real del video en 1x {0} min'.format(all_time_duration_play_list/60.0))
						print('Velocidad reproduccion 2x activado')
						all_time_duration_play_list = all_time_duration_play_list/2.0 
						activate_two_speed_play_video = True
					# if activate_two_speed_play_video:
					# 	all_time_duration_play_list = all_time_duration_play_list/2.0 
					if count_viewers == 0:
						print('Verificacando interacciones en la 1ra iteracioón>')
						self.click_stadistic()
					print ('Esperando a que reproduzca {0} min'.format(all_time_duration_play_list/60.0))
					time.sleep(all_time_duration_play_list+10) #mas 10s de extra
					counter_for +=1
				except Exception as e:
					print ('Error al ubicar xpath de ver todos los videos..', e )
				time.sleep(5)

			# guardamos el registro de renovaciones en log
			# f = open(PATH_LOG, 'a')
			# mensaje = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') + " : x-csrf-token :" + \
			#  str(self.headers.get('x-csrf-token')) + ": x-guest-token : " + str(self.headers.get('x-guest-token'))
			# f.write('\n' + mensaje)
			# f.close()
			self.driver.close()
			self.driver.quit()
		except Exception as e:
			print ('Error en procesar cookies>', e)
		return None, None, None

count_viewers = 0
while True:
	try:
		entity_youtue_viewer = YoutubeViewerRobot()
		if count_viewers==0:
			username='iisotecperu@gmail.com'
			password='Iisotec2020#$%'
			# auth_google = AuthGoogle(username,password)
			entity_youtue_viewer.init_chrome(is_auth=True)
			# entity_youtue_viewer.init_chrome(is_auth=True, username=username, password=password)
			# driver = auth_google.login_google()
		else:
			entity_youtue_viewer.init_chrome()
		list_channels = ['https://www.youtube.com/channel/UCvKo8kmdoyW38lHGaqBfGuQ/videos',
		'https://www.youtube.com/channel/UCkVPuYiqd2QzGuOWLzVe3Nw/videos',
		'https://www.youtube.com/channel/UCbX3gql5awyj6_60HOsuigg/videos',
		'https://www.youtube.com/channel/UCriyhRhNvOMyVlEYZFDXrUA/videos']
		entity_youtue_viewer.get_open_browser(list_channels, count_viewers)
		print ('Esperando....')
		count_viewers +=1 
		time.sleep(randint(15, 30))
	except Exception as e:
		print ('Error >>', e)
	print('Itracion>',count_viewers)
	time.sleep(5)
		
