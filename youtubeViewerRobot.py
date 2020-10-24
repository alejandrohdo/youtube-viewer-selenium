import json
import os
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
import time
from random import randint
from selenium.webdriver.common.keys import Keys 

class YoutubeViewerRobot():
	"""Script que permite acceder a youtube y visualizar los videos por canal"""
	def __init__(self):
		self.headers = {
			'authority': 'api.twitter.com',
			'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
			'x-twitter-client-language': 'es',
			'x-csrf-token': '04773c23a3b4735b19ae02c481b463f3',
			'x-guest-token': '1317467561395703810',
			'x-twitter-active-user': 'yes',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			'accept': '*/*',
			'origin': 'https://twitter.com',
			'sec-fetch-site': 'same-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://twitter.com/search?f=live&q=VIZCARRA lang:es&src=typed_query',
			'accept-language': 'es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7',
			'cookie': 'personalization_id="v1_VJQSdKRys2+7shiTS+TV+Q=="; guest_id=v1%3A160263196834131478; gt=1317467561395703810; ct0=04773c23a3b4735b19ae02c481b463f3;',
		}

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

	def extract_time_duration_play_list(self,driver):
		try:
			print ('Extrayendo tiempos..')
			xpath = '//*[@id="playlist-items"]/a/div/div[2]//ytd-thumbnail-overlay-time-status-renderer//span'
			list_time = driver.find_elements_by_xpath(xpath)
			time.sleep(1)
			new_list_time  = []
				# list_time.append(time)
			for time_l in list_time:
				new_list_time.append(time_l.text)
			return self.caculate_all_duration_time_play_list(new_list_time)
			# print ('LIST TIME>', new_list_time)
		except Exception as e:
			print ('Error time play list>', e)

	def two_speed_play_video(self, driver):
		'''Aumenta la velociadad de reproduccion a 2x'''
		try:
			xpath_config_video = '//*[@id="movie_player"]/div[25]//button[3]'
			xpath_playback_speed = "//div[contains(@class, 'ytp-popup ytp-settings-menu')]/div/div[1]/div[2]"
			#velocidad al final de xpath> div[8]=2, div[7]=1.75, div[6]=1.5,etc.
			driver.find_element_by_xpath(xpath_config_video).click() #click config
			time.sleep(0.5)
			driver.find_element_by_xpath(xpath_playback_speed).click() #click velocidad reproduccion
			time.sleep(0.5)
			xpath_playback_down = "//div[contains(@class, 'ytp-popup ytp-settings-menu')]/div/div/div[8]"
			driver.find_element_by_xpath(xpath_playback_down).click()
			time.sleep(0.5)
			driver.find_element_by_xpath(xpath_config_video).send_keys(Keys.ESCAPE)
			# driver.find_element_by_xpath(xpath_playback_down).send_keys(Keys.DOWN)
			return True
		except Exception as e:
			print ('Error xpath speed>', e)
		return False


	def get_open_browser(self, list_channels):
		"""Funcion que visita a twitter"""
		try:
			PATH_CHROMEDRIVER = '/home/alejandro/Downloads/chromedriver_linux64-2/chromedriver'
			PATH_LOG = self.get_path_base_driver() +"/app/tweet/log/log_renovate_cookie_twitter.txt"
			chrome_options = webdriver.ChromeOptions()
			# chrome_options.add_argument('--no-sandbox')
			# chrome_options.add_argument("--headless")
			chrome_options.add_argument("--mute-audio")
			# chrome_options.add_argument('--disable-extensions')
			# chrome_options.add_argument('--dns-prefetch-disable')
			# estrategia de carga
			# options = Options()
			# options.page_load_strategy = 'eager' # defecto = 'normal',  y None
			driver = webdriver.Chrome(
			    # desired_capabilities=caps,
			    # options=options,
			    chrome_options=chrome_options,
			    executable_path=PATH_CHROMEDRIVER)
			counter_for = 0 # solo para activar 2x por primeva vez
			activate_two_speed_play_video = False
			for channel in list_channels:
				print ('Visitando..', channel)
				driver.get(channel)
				try:
					xpath_view_video  = '//*[@id="play-all"]/ytd-button-renderer'
					driver.find_element_by_xpath(xpath_view_video).click()
					time.sleep(20)
					all_time_duration_play_list = self.extract_time_duration_play_list(driver)
					if counter_for ==0:
						print ('Aumentado velocidad de reproduccion')
						is_two_speed_play_video =  self.two_speed_play_video(driver)
						if is_two_speed_play_video and all_time_duration_play_list>0:
							print ('Duracion real del video en 1x {0} min'.format(all_time_duration_play_list/60.0))
							print('Velocidad reproduccion 2x activado')
							all_time_duration_play_list = all_time_duration_play_list/2.0 
							activate_two_speed_play_video = True
					if activate_two_speed_play_video:
						all_time_duration_play_list = all_time_duration_play_list/2.0 
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
			driver.close()
			driver.quit()
		except Exception as e:
			print ('Error en procesar cookies>', e)
		return None, None, None


while True:
	try:
		a = YoutubeViewerRobot()
		list_channels = ['https://www.youtube.com/channel/UCvKo8kmdoyW38lHGaqBfGuQ/videos',
		'https://www.youtube.com/channel/UCkVPuYiqd2QzGuOWLzVe3Nw/videos',
		'https://www.youtube.com/channel/UCbX3gql5awyj6_60HOsuigg/videos',
		'https://www.youtube.com/channel/UCriyhRhNvOMyVlEYZFDXrUA/videos']
		a.get_open_browser(list_channels)
		print ('Esperando....')
		time.sleep(randint(15, 30))
	except Exception as e:
		print ('Error >>', e)
		
