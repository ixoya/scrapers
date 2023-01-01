#!/usr/bin/python3
# < ivn > | https://keybase.io/ixoya

import json
import requests
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

session = requests.Session()
parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, required=True)
parser.add_argument('--dir', type=str, required=False)
args = parser.parse_args()

def Scraper(url):
    r = session.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    scripts = soup.find("script", {"type":"application/json"})
    urlList= []
    for url in scripts:
        files = json.loads(url)
        for key , items in files.items():
            if key == "props":
                item = items.get("pageProps")
                item2 = item.get("album")
                item3 = item2.get("files")
                length = len(item3)              
                for item in range(length):
                    name = item3[item].get('name')
                    cdnUrl = item3[item].get('cdn')
                    cdn = cdnUrl.strip("https://cdn.bunkr.ru")
                    if cdn == "":
                        url = "https://media-files.bunkr.ru/" + name
                        urlList.append(url)
                    else:
                        url = f"https://media-files{cdn}.bunkr.ru/" + name
                        urlList.append(url)
                return urlList


def Downloader():
    urlList = Scraper(args.url)
    for url in urlList:
        name = url.split('/')[-1]
        if args.dir:
            if args.dir[-1] == '/':
                args.dir = args.dir[:-1]
            outDir = str(args.dir) + '/' + str(args.url.split('/')[-1])
            outputDir = Path(outDir)
            outputDir.mkdir(exist_ok=True)
        else:
            outputDir = Path(args.url.split('/')[-1])
            outputDir.mkdir(exist_ok=True)
        r = requests.get(url)
        if r.status_code != 200:
            print(f"Failed -  {name}")
        else:
            print(f"Downloading - {name}")
            with open(str(outputDir / name), 'wb') as f:
                f.write(r.content)


if __name__ == "__main__":
    Downloader()
