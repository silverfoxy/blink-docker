import time, sys
from selenium import webdriver
from pyvirtualdisplay import Display
from BrowserHandler import BrowserHandler

def main() :
	if len(sys.argv) < 2 :
		print('Usage: ')
		print(sys.argv[0] + ' BrowserName')
		return
	selected_browser = sys.argv[1]
	print('Using ' + sys.argv[1])
	browser_handler = BrowserHandler()
	driver = browser_handler.get_driver(selected_browser)
	driver.get("https://silverf0x00.com")
	time.sleep(10)
	driver.save_screenshot('/home/blink/Downloads/result.png')
	driver.get_screenshot_as_png()
	with open('/home/blink/Downloads/result.html', "wb") as fout:
	    fout.write(driver.page_source.encode("utf-8"))
	    fout.flush()

if __name__ == '__main__' :
	main()
