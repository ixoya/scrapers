#!/usr/bin/python3
# < ivn > | https://keybase.io/ixoya

import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, required=True)
parser.add_argument("--write-file", default=False, action="store_true")
parser.add_argument("--site", type=str, required=False)
args = parser.parse_args()

headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'upgrade-insecure-requests': '1',
        'te': 'trailers'
}

if args.site:
    baseurl = f"https://{args.site}"
else:
    baseurl = "https://1337x.to"

def getpageCount(username):
    url = baseurl + "/user/" + username + "/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    lastPage = soup.find('div', {'class': 'pagination'})
    pageCount = int(lastPage.findAll('a')[-1]['href'].split('/')[-2])
    return pageCount


def getallTorrents():
    pageCount = getpageCount(args.username)
    for page in range(1, pageCount + 1):
        url = f"{baseurl}/{args.username}-torrents/{page}/" 
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        torrentList = soup.select('a[href*="/torrent/"]')
        for torrent in torrentList:
            name = torrent.getText().strip()
            torrenturl = baseurl + str(torrent["href"])
            m = requests.get(torrenturl, headers=headers)
            msoup = BeautifulSoup(m.content, 'html.parser')
            magnetLink = msoup.select('a[href^="magnet"]')
            magnetLink = magnetLink[0]['href'] if magnetLink else None
            if args.write_file:
                with open(f'{args.username}.txt', 'a') as file:
                    text = f"{str(torrenturl)} - {str(magnetLink)}\n\n"
                    file.write(text)
                    file.close()
            else:
                print(f"{name} - {magnetLink}")
            


if __name__ == "__main__":
    getallTorrents()
