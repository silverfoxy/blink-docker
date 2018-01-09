#!/usr/bin/python3
# -*-coding:utf-8 -*

import subprocess, glob

#Browsers dictionary
browsersDict = {
    'FirefoxRepo',
    'Firefox',
    'FirefoxESR',
    'Chrome',
    'Chromium',
    'Opera'
}

class ScriptsHandler() :
    def __init__(self, browser_name, scripts_path = None) :
        if scripts_path == None :
            self.scripts_path = '/home/blink/Downloads/scripts/'
        else :
            self.scripts_path = scripts_path
        self.browser_name = browser_name

    # List of python files in specified directory
    def find_scripts(self, dir) :
        return glob.glob(dir + '*.py') 
    def run(self) :
        try :
            scripts = self.find_scripts(self.scripts_path)
            for script in scripts :
                # Run all scripts but BrowserHandler.py
                if "BrowserHandler" not in script :
                    print('Running %s' % script)
                    try :
                        subprocess.check_call(['python3', script, self.browser_name])
                    except Exception as e :
                        print(e)
                    finally :
                        print('Done.')
        except Exception as e :
            print(e)

if __name__ == '__main__' :
    runSelenium = ScriptsHandler(browserDict[2])
    runSelenium.run()