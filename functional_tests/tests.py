from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from time import sleep, time

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()	

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def wait_for_row_in_list_table(self, row_text):
		start_time = time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
				
			except(AssertionError, WebDriverException) as e:
				if time() - start_time > MAX_WAIT:
					raise e
				sleep(0.5)

	def test_can_start_a_list_for_one_user(self):

		self.browser.get(self.live_server_url)

		self.assertIn('A-Fazer', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('A-Fazer', header_text)

		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
						input_box.get_attribute('placeholder'), 
						'Digite seu A-Fazer'
						)
		input_box.send_keys('Comprar um desmafagafador')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Comprar um desmafagafador')
		
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Usar o desmafagafador em um mafagafo')
		input_box.send_keys(Keys.ENTER)
		sleep(1)

		self.wait_for_row_in_list_table('2: Usar o desmafagafador em um mafagafo')
		self.wait_for_row_in_list_table('1: Comprar um desmafagafador')


	def test_mutiple_users_can_start_lists_at_different_urls(self):
		#PRIMEIRO USUARIO
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Comprar desmafagafador')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Comprar desmafagafador')

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#SEGUNDO USUARIO
		self.browser.quit()
		self.browser = webdriver.Firefox()

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Comprar um desmafagafador', page_text)
		self.assertNotIn('Usar o desmafagafador em um mafagafo', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Comprar mel')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Comprar mel')

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Comprar um desmafagafador', page_text)
		self.assertIn('Comprar mel', page_text)
		

	def ignore_test_finnish_tests(self):
		self.fail('Acabaram os testes!!')

