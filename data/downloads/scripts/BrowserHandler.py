# This script is not run automatically, you have to import it in your running scripts
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#Browsers dictionary
browsersDict = [
    'FirefoxRepo',
    'Firefox',
    'FirefoxESR',
    'Chrome',
    'Chromium',
    'Opera'
]

class BrowserHandler() :
	def __init__(self, display_size = (1920, 1080), display_visible = 0) :
		self.display = Display(visible = display_visible, size = display_size)
	def setup_driver(self, browser_name) :
		self.display.start()
		if browser_name == browsersDict[0] : #FirefoxRepo
			profile = webdriver.FirefoxProfile("/home/blink/.mozilla/firefox/blink.default")
			ffesr_binary = FirefoxBinary('firefox')
			driver = webdriver.Firefox(profile, firefox_binary=ffesr_binary)
			return driver
		elif browser_name == browsersDict[1] : #Firefox
			profile = webdriver.FirefoxProfile("/home/blink/.mozilla/firefox/blink.default")
			ffesr_binary = FirefoxBinary('/home/blink/browsers/firefox-latest/firefox')
			driver = webdriver.Firefox(profile, firefox_binary=ffesr_binary)
			return driver
		elif browser_name == browsersDict[2] : #FirefoxESR
			profile = webdriver.FirefoxProfile("/home/blink/.mozilla/firefox/blink.default")
			ffesr_binary = FirefoxBinary('/home/blink/browsers/firefox-latest-esr/firefox')
			driver = webdriver.Firefox(profile, firefox_binary=ffesr_binary)
			return driver
		elif browser_name == browsersDict[3] : #Chrome
			# --password-store=basic --load-extension= --no-default-browser-check --no-first-run
			options = webdriver.ChromeOptions()
			options.add_argument("/home/blink/browsers/extensions/ups/")
			options.binary_location = "/home/blink/browsers/chrome/opt/google/chrome/chrome"
			driver = webdriver.Chrome(chrome_options = options)
			return driver
		elif browser_name == browsersDict[4] : #Chromium
			options = webdriver.ChromeOptions()
			options.add_argument("/home/blink/browsers/extensions/ups/")
			options.binary_location = "/usr/bin/chromium-browser"
			driver = webdriver.Chrome(chrome_options = options)
			return driver
		elif browser_name == browsersDict[5] : #Chromium
			raise Exception('Opera is currently not supported by our Selenium script on Blink')
		else :
			raise Exception('Unsupported browser name')
	def get_driver(self, browser_name) :
		driver = self.setup_driver(browser_name)
		return driver
	def get_writable_dir(self) :
		return '/home/blink/Downloads/'