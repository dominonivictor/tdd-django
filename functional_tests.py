from selenium import webdriver
import unittest as ut


class NewVisitorTest(ut.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('A-Fazer', self.browser.title)
		self.fail('Acabar o teste!!')

if __name__ == '__main__':
	ut.main(warnings='ignore')
