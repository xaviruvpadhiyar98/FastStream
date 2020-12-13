#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
from os import system


base_url = 'https://1337x.to'
page = '1'

# Just Some Random User-Agent
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 ADG/11.0.2978 Safari/537.36',
}

# proxy-setup if any
PROXY_HOST = 'zproxy.lum-superproxy.io' 
PROXY_PORT = 22225
PROXY_USER = 'lum-customer-moovitdpt1-zone-birdsfresidential-session-$session'
PROXY_PASS = 'x76b2glbaq0k'
proxies = {'https':f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'}


def main(search):
    # Getting The First Page Results 
    response = requests.get(f'{base_url}/search/{search}/{page}/', headers=headers)
    tree = html.fromstring(response.content)
    MoviesTvShowName = tree.xpath('//td/a[2]/text()')
    MoviesTvShowLink = tree.xpath('//td/a[2]/@href')
    MoviesTvShowSize = tree.xpath('//td[5]/text()')
    for i,x in enumerate(zip(MoviesTvShowName,MoviesTvShowSize)):
        print(str(i)+'\t',x[0][:40]+'\t'+x[1])

    # Choose A Number to Play That Movie/Series
    MoviesTvShowChoose = int(input('Choose Proper Number To Play - '))
    print('Playing .. - ' + MoviesTvShowName[MoviesTvShowChoose])

    # Searching for .torrent file
    response2 = requests.get(f'{base_url}{MoviesTvShowLink[MoviesTvShowChoose]}', headers=headers)
    tree2 = html.fromstring(response2.content)
    for x in tree2.xpath('//a/@href'):
        if x.endswith('.torrent'):
            x = x.replace('http','https')
            break

    MoviesTvShowFileName = 'TorrentFiles/' + MoviesTvShowName[MoviesTvShowChoose].split()[0] +'.torrent'

    # Downloading the .Torrent File
    with open(MoviesTvShowFileName,'wb') as f:
        r = requests.get(x,headers=headers,proxies=proxies)
        f.write(r.content)

    # Opening VLC Player
    MoviesTvShowPlayCMD = 'vlc '+ MoviesTvShowFileName
    system(MoviesTvShowPlayCMD)

if __name__ == '__main__':
    search = input('Enter TV/Movie Name To Search - ').replace(' ','+')
    main(search)    

