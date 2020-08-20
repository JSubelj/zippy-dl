#!/usr/bin/env python3

import concurrent.futures
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib import request, parse
import os
import subprocess
import pathlib
import shutil

ROOT = pathlib.Path(__file__).parent.absolute()
CHROME_URL = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F800100%2Fchrome-linux.zip?alt=media"
CHROME_DRIVER_URL = "https://chromedriver.storage.googleapis.com/85.0.4183.38/chromedriver_linux64.zip"
S7ZIP_PATH=os.path.join(ROOT,"7z_binary/7z")
CHROMIUM_PATH=os.path.join(ROOT,"chrome-linux/chrome")
CHROMIUMDRIVER_PATH=os.path.join(ROOT,"chromedriver")


import argparse

def check_download_extract_chromediver():
    def download_chromedriver():
        print("Downloading chrome driver")
        request.urlretrieve(CHROME_DRIVER_URL, os.path.join(ROOT,"chromiumdriver.zip"))

    def extract_chromedriver():
        print("Extracting chrome driver to", ROOT)
        subprocess.run([S7ZIP_PATH,"x",f"{os.path.join(ROOT,'chromiumdriver.zip')}",f"-o{ROOT}","-aoa"],stdout=subprocess.DEVNULL)

    def chrome_driver_exists():
        return os.path.exists(os.path.join(ROOT,CHROMIUMDRIVER_PATH))


    if not chrome_driver_exists():
        download_chromedriver()
        extract_chromedriver()

def check_download_extract_chromium():
    def download_chromium():
        print("Downloading chromium")
        request.urlretrieve(CHROME_URL, os.path.join(ROOT,'chromium.zip'))


    def chromium_exists():
        return os.path.exists(CHROMIUM_PATH)

    def extract_chromium():
        print("Extracting chromium to", ROOT)
        subprocess.run([S7ZIP_PATH,"x",f"{os.path.join(ROOT,'chromium.zip')}",f"-o{ROOT}","-aoa"],stdout=subprocess.DEVNULL)

    if not chromium_exists():
        download_chromium()
        extract_chromium()





if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Downloads a file from zippyshare')
    parser.add_argument('-f', "--file", help='File with urls separated by newline', default=None)
    parser.add_argument('url', nargs="?", help='an integer for the accumulator')
    parser.add_argument('-o', "--output", default=os.getcwd(), help='Output directory (default: \'.\')')

    args = parser.parse_args()

    # MAKES 7z RUNNABLE
    subprocess.run(["chmod","u+x",S7ZIP_PATH])

    def download(url):
        options = webdriver.ChromeOptions()
        options.binary_location = CHROMIUM_PATH
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=CHROMIUMDRIVER_PATH, options=options)
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dlbutton"))
        )
        href = element.get_attribute("href")
        driver.quit()
        name = parse.unquote(href.split("/")[-1])
        print("Starting downloading "+name)
        local_filename, headers = request.urlretrieve(href,os.path.join(ARCHIVE_PATH,name))
        print("Finished downloading "+name)
        print("Starting extracting "+name)
        subprocess.run([S7ZIP_PATH,"x",f"{local_filename}",f"-o{args.output}","-aoa"],stdout=subprocess.DEVNULL)
        print("Extracted "+name)


    urls = []
    if args.file:
        with open(args.file) as f:
            for line in f:
                urls.append(line)
    else:
        if args.url:
            urls.append(args.url)

    if not len(urls):
        print("ERROR: At least one url needs to be provided")
        parser.print_help()
        exit(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: x(), [check_download_extract_chromediver, check_download_extract_chromium])



    if not os.path.exists(os.path.join(args.output,"archives_zippydl")):
        print("Creating temporary directory",os.path.join(args.output,"archives_zippydl"))
        os.mkdir(os.path.join(args.output,"archives_zippydl"))

    ARCHIVE_PATH = os.path.join(args.output,"archives_zippydl")

    paths = []
    print("Downloading files")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download,urls)

    shutil.rmtree(ARCHIVE_PATH)


