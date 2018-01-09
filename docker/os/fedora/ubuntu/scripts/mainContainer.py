#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import random
import subprocess
import numpy
import utils
import time
import csv
from chrome import *
from firefox import *
from rws import *
from browsersList import browsersList

# Selenium imports
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import runSeleniumScripts

############### Container Class
class Container(object):

    ### Environment variables
    homeFolder = '/home/blink/'
    allPluginsFolder = homeFolder+'plugins/'
    allFontsFolder = homeFolder+'fonts/'
    allBrowsersFolder = homeFolder+'browsers/'

    profileFolder = homeFolder+'profile/'
    dataFile = profileFolder+'data.json'
    encryptedDataFile = dataFile+".gpg"
    updateFile = profileFolder+"update"
    fontsCSVFile = homeFolder+'fontsWeightBlink.csv'
    pluginsCSVFile = homeFolder+'pluginsWeightBlink.csv'

    destFontsFolder = '/home/blink/.fonts/'
    destPluginsFolder = '/home/blink/.mozilla/plugins/'

    #Numbers updated (29th October) from Linux FPs
    averageNbFonts = 155.556
    sdFonts = 127.488
    averageNbPlugins = 4.297
    sdPlugins = 3.269

    #Browsers dictionary
    browsersDict = {
        'FirefoxRepo': FirefoxRepo,
        'Firefox':Firefox,
        'FirefoxESR':FirefoxESR,
        'Chrome':Chrome,
        'Chromium':Chromium
        #'Opera':Opera
    }

    ### Init
    def __init__(self):

        #List of plugins
        self.pluginsList = Container.readCsvFile(Container.pluginsCSVFile)

        #List of fonts
        self.fontsList = Container.readCsvFile(Container.fontsCSVFile)

    ### PLUGINS
    def selectPlugins(self):
        nbRandomPlugins = int(numpy.random.normal(loc=Container.averageNbPlugins,scale=Container.sdPlugins))
        while nbRandomPlugins < 1 :
            nbRandomPlugins = int(numpy.random.normal(loc=Container.averageNbPlugins,scale=Container.sdPlugins))

        pluginsRWS = RWS(self.pluginsList)

        #We chose randomly nbRandomPlugins plugins
        chosenPlugins = pluginsRWS.getRandomItems(nbRandomPlugins)

        #We remove old mozilla files to be sure to correctly load plugins
        subprocess.call("find ~/.mozilla -name pluginreg.dat -type f -exec rm {} \;", shell=True)

        #We remove the links to the old plugins and create symbolic links for the new ones
        subprocess.call("rm -rf "+Container.destPluginsFolder+"*",shell=True)
        for plugin in chosenPlugins:
            subprocess.call(["ln","-s",Container.allPluginsFolder+plugin,Container.destPluginsFolder+plugin])

    ### FONTS
    def selectFonts(self):
        nbRandomFonts = int(numpy.random.normal(loc=Container.averageNbFonts,scale=Container.sdFonts))
        while nbRandomFonts < 1:
            nbRandomFonts = int(numpy.random.normal(loc=Container.averageNbFonts,scale=Container.sdFonts))

        fontsRWS = RWS(self.fontsList)

        #We chose randomly nbRandomFonts fonts
        chosenFonts = fontsRWS.getRandomItems(nbRandomFonts)

        #We create symbolic links for the new ones
        subprocess.call("rm -rf "+Container.destFontsFolder+"*",shell=True)
        for font in chosenFonts:
            subprocess.call(["ln","-s",Container.allFontsFolder+font,Container.destFontsFolder+font])

    ### BROWSERS
    @staticmethod
    def selectBrowser():
        #We chose a browser from the ones provided by each OS
        selectedBrowser = browsersList[random.randint(0,len(browsersList)-1)]
        #return Container.browsersDict[selectedBrowser]()
        # Always run FirefoxESR for now
        #selectedBrowser = browsersList[5]
        print('-' + selectedBrowser)
        return selectedBrowser, Container.browsersDict[selectedBrowser]()

    ### Check existence of data file
    # If the file does not exist, it is created
    # If the file is encrypted, it will be unencrypted
    @staticmethod
    def checkDataFile():
        if os.path.isfile(Container.encryptedDataFile):
            #We decrypt it
            cancelled = False
            while not os.path.isfile(Container.dataFile) and not cancelled:
                res = subprocess.getstatusoutput("gpg2 -d -o "+Container.dataFile+" "+Container.encryptedDataFile)
                if res[0] != 0 and "cancelled" in res[1]:
                    cancelled = True
            subprocess.call("rm "+Container.encryptedDataFile,shell=True)
        elif not os.path.isfile(Container.dataFile):
            jsonData = {"bookmarks":
                            [{"name":"Bookmarks Toolbar","children":[],"type":"folder"},
                             {"name":"Bookmarks Menu","children":[],"type":"folder"},
                             {"name":"Unsorted Bookmarks","children":[],"type":"folder"}],
                        "openTabs":[],
                        "passwords":[],
                        "passwordStorage":False,
                        "passwordEncryption":False,
                        "refresh": False,
                        "browser":"Firefox"}
            utils.writeJSONDataFile(jsonData,Container.dataFile)

    ### CSV FILE
    # Import plugins/fonts weight from
    # CSV file
    @staticmethod
    def readCsvFile(path):
        #########
        # Format
        # 1 - Name of font/plugin
        # 2 - Name of file
        # 3 - Weight
        #########
        l = []
        with open(path, newline='') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                l.append((row[0],row[1],int(row[2])))
        return l

# Run single script
def runSelenium(script_name = None) :
    display = Display(visible = 0, size = (1920, 1080))
    display.start()
    profile = webdriver.FirefoxProfile("/home/blink/.mozilla/firefox/blink.default")
    ffesr_binary = FirefoxBinary('/home/blink/browsers/firefox-latest-esr/firefox')
    driver = webdriver.Firefox(profile, firefox_binary=ffesr_binary)
    driver.get("https://amiunique.org/fp")
    time.sleep(10)
    driver.save_screenshot('/home/blink/Downloads/result.png')
    driver.get_screenshot_as_png()
    with open('/home/blink/Downloads/result.html', "wb") as fout:
        fout.write(driver.page_source.encode("utf-8"))
        fout.flush()

# Run all scripts in specified directory
def runAllSeleniumScripts(selected_browser, scripts_dir = None) :
    scriptHandler = runSeleniumScripts.ScriptsHandler(selected_browser, scripts_dir)
    scriptHandler.run()

############### Main
def main():
    print("Blink Container Main script")

    #Change the working directory to the Shared folder
    os.chdir(Container.homeFolder)

    if os.path.isfile(Container.updateFile):
        #We update the container
        subprocess.call(["python3","/home/blink/updateContainer.py"])
    else :
        #We create an instance of Container
        blink = Container()

        #We check the Data file with the complete user profile
        blink.checkDataFile()

        #We initialise a boolean to indicate if the
        #container must be shutdown
        shutdown = False

        while not shutdown :
            #We chose the fonts and the plugins
            blink.selectFonts()

            #We chose the browser
            browserName, browser = blink.selectBrowser()

            #We chose the plugins only if it is Firefox
            if isinstance(browser,FirefoxBase):
                blink.selectPlugins()

            #We import the user profile inside the browser
            browser.importData()

            #We launch the browser
            #browserProcess = browser.runBrowser()

            # Run selenium scripts
            runAllSeleniumScripts(browserName)

            # Get into bash for debugging purposes
            #subprocess.call(["/bin/bash"])

            #We wait for either the browsing session to be finished
            #while not isinstance(browserProcess.poll(),int):
            #    time.sleep(1)

            encryption,refresh = browser.exportData()

            #We refresh the fingerprint if refresh has been demanded
            if not refresh:
                #Encrypt file if the encryption is activated
                if encryption :
                    done = False
                    while not done :
                        res = subprocess.getstatusoutput("gpg2 -c --cipher-algo=AES256 "+Container.dataFile)
                        if res[0] == 0 :
                            #If the encryption went well, we removed the unencrypted file
                            subprocess.call("rm "+Container.dataFile,shell=True)
                            done = True
                        elif "cancelled" in res[1]:
                            #If the user cancelled the encryption operation, we do nothing
                            done = True

                #We finish the execution of the script
                shutdown = True

if __name__ == "__main__":
    main()
