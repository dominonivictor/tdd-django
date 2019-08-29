from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest as ut
from time import sleep


class NewVisitorTest(ut.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')

		title_text = self.browser.title
		self.assertIn('A-Fazer', title_text)
		
		header_text = self.browser.find_element_by_tag_name('h1'.text)
		self.assertIn('A-Fazer', header_text)

		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
						input_box.get_attribute('placeholder'), 
						'Digite seu A-Fazer')
		input_box.send_keys('Comprar um desmafagafador')
		input_box.send_keys(Keys.ENTER)
		sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.browser.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Comprar um desmafagafador' for row in rows)
			)

		self.fail('Acabar o teste!!')

if __name__ == '__main__':
	ut.main(warnings='ignore')
