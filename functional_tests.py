from selenium import webdriver

#browserPath = "/usr/local/share/gecko_driver/"
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title