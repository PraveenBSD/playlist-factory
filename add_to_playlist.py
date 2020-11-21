import logging
import selenium
import os
import json
import time
from elements_path import *


configFilePath = "config/config.json"
youtubeSearchURL = "https://www.youtube.com/results?search_query="
youtubeURL = "https://www.youtube.com"

def LoadConfig(logging):
    f = open(configFilePath, "r")
    config = json.loads(f.read())
    f.close()
    for k, v in config.items():
        if v == "":
            logging.error(k, " config value cant be empty")
            exit()
        
    return config

def LoadData(filePath):
    f = open(filePath, "r")
    respJson = json.loads(f.read())
    f.close()
    return respJson

def SignIn(driver, userName, password):
    driver.get(youtubeURL)
    driver.find_element_by_xpath(signInButton).click()
    driver.find_element_by_xpath(userNameBox).send_keys(userName)
    driver.find_element_by_xpath(nextButton).click()
    time.sleep(2)
    driver.find_element_by_xpath(passwordBox).send_keys(password)
    driver.find_element_by_xpath(loginButton).click()
    time.sleep(4)

def AddToPlaylist(logging, driver, segments, playlistName):
    for segment in segments:
        try:
            logging.info("adding video ", segment["title"])
            driver.get(youtubeSearchURL + segment["title"] + " SNL")

            elements = driver.find_elements_by_id("video-title")

            url = elements[0].get_attribute("href")
            elements[0].click()
            time.sleep(2)

            texts = driver.find_elements_by_id("button")
            for textele in texts:
                if textele.get_attribute("aria-label") == "Save to playlist":
                    textele.click()
                    break
            time.sleep(2)

            playlistFound = False
            playlists = driver.find_elements_by_tag_name("yt-formatted-string")
            for playlist in playlists:
                if playlist.text == playlistName:
                    playlistFound = True
                    playlist.click()

            if not playlistFound:
                logging.error(playlistName, " playlist not found")
                exit()

            time.sleep(2)
            logging.info("added url ", url)

        except Exception as e:
            logging.error("error while adding video ", segment["title"], e)


if __name__ == '__main__':
    logging.basicConfig(filename="add_to_playlist.log", level=logging.INFO)
    
    logging.info("loading config...")
    config = LoadConfig(logging=logging)

    chrome_driver = os.getcwd() +"/" + config["chromeDriverRelativePath"]
    logging.info("initializing driver")
    driver = selenium.webdriver.Chrome(executable_path=chrome_driver) 

    logging.info("loading data...")
    segments = LoadData(filePath=config["filePath"])["segments"]

    logging.info("Signing In")
    SignIn(driver=driver, userName=config["userName"], password=config["password"])

    logging.info("Starting to add videos to playlist ", config["playlistName"])
    AddToPlaylist(logging=logging, driver=driver, segments=segments, playlistName=config["playlistName"])    

    logging.info("closing driver")
    driver.close()

    exit()

