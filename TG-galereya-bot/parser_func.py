import requests
import re
from bs4 import BeautifulSoup
import os

#################################################################

URL = 'https://opisanie-kartin.com/vse-opisaniya/?pg=1'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0', 'accept' : '*/*'}
HOST = 'https://opisanie-kartin.com/'

web_art = ''
author = ''
art = ''
no_info = 0

def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_description_link(html):
    stop = 0
    page = 1
    global web_art
    global author
    global art
    global no_info
    no_info = 0
    name_author_ = open(f"D:\\Python\\TG-galereya-bot\\text\\text_author.txt", "r", encoding='windows 1251')
    name_art_ = open(f"D:\\Python\\TG-galereya-bot\\text\\text_art.txt", "r", encoding='windows 1251') 
    author = str(name_author_.readlines())[2:-2]
    art = str(name_art_.readlines())[2:-2]
    name_author_.close()
    name_art_.close()
    print(author)
    print(art)
    soup = BeautifulSoup(html, 'html.parser')
    while stop == 0:
        key = soup.find_all(attrs={"title": f'Описание картины {author} «{art}»'})
        if key:
            index_title = str(key).find('" title')
            web_art = str(key)[10:index_title]
            break
        else:
            page = page + 1
            html = get_html(URL, params={'pg': page})
            soup = BeautifulSoup(html.text, 'html.parser')
            if page == 9:
                no_info = 1
                print("There is no info you need. I'm sorry...")
                break
            continue
    return no_info, author, art, web_art, print('get_description_link END ' + (web_art)) if web_art != '' else print('something wrong...')

def get_content(html):
    global HOST
    global no_info
    if no_info == 1:
        return no_info
    else:
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('p')
        info = []
        img = soup.select_one('img[src*=".jpg"]')["src"]
        print('img is')
        with open(f"D:\\Python\\TG-galereya-bot\\images\\img.jpg", "wb") as imag:
            imag.write(requests.get('https://opisanie-kartin.com'+img).content)
            imag.close()

        for item in items:
            info.append(
                item.get_text()
                )
        len_info = len(info)
        info = info[2:(len_info-3)]
        print('Нужная инфа собрана в лист')
        print(info)
        return info

def get_info():
    global no_info
    URL = 'https://opisanie-kartin.com/vse-opisaniya/?pg=1'
    html = get_html(URL)
    print(html)
    if html.status_code == 200:
        print("Я подключился к сайту с инфой!")
        get_description_link(html.text)
        if no_info == 1:
            print(no_info)
            return no_info
        elif no_info == 0:
            URL_2 = web_art
            html = get_html(URL_2)
            content = get_content(html.text)
            for x, y in ("\n", ""), ('[', ""), (']', ''), ("', '",''):
                content = str(content).replace(x, y)
            return content
        else:
            print('Произошла ошибка, соре')
    
########################################################