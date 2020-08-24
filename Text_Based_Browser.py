import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore

args = sys.argv
direction_name = args[1]
back_stack = deque()
tab = {}
page_ = ''
new_text = ''

if not os.path.isdir(direction_name):
    os.mkdir(direction_name)


def http_adder(text):
    if not text.startswith('http://') and not text.startswith('https://'):
        text = 'http://' + text
    return text


def tab_save(text):
    global tab
    global new_text
    if text.startswith('https://'):
        new_text = text.replace('https://', '')
    elif text.startswith('http://'):
        new_text = text.replace('http://', '')
    else:
        new_text = text
    domains = ['.com', '.net', '.org', '.gov', '.uk', '.us', '.ru', '.edu', '.co', '.ir', '.com/',
               '.net/', '.org/', '.gov/', '.uk/', '.us/', '.ru/', '.edu/', '.co/', '.ir/']
    for domain in domains:
        if new_text.endswith(domain):
            new_text = new_text.replace(domain, '')
    if 'www.' in new_text:
        new_text = new_text.replace('www.', '')
    d = {new_text: text}
    tab.update(d)


def tab_view(text):
    if len(tab) > 0:
        for tab_item in tab:
            if text == tab_item:
                return tab[text]
    else:
        return None


def back_save(text):
    text = http_adder(text)
    back_stack.append(text)


def back_view(text):
    if text.lower() == 'back':
        if not len(back_stack) == 0 and not len(back_stack) == 1 and \
                not back_stack[0] == 'https://back' and not back_stack[0] == 'http://back':
            back_stack.pop()
            return back_stack.pop()
    else:
        return None


def file_name(text):
    if text.startswith('https://'):
        text = text.replace('https://', '')
    elif text.startswith('http://'):
        text = text.replace('http://', '')
    if '.' in text:
        text = text.replace('.', '_')
    if text.endswith('/'):
        text = text.replace('/', '')
    return text


def file_save(content, path, file_name_):
    with open('{}/{}.txt'.format(path, file_name_), 'w', encoding='utf-8') as f:
        f.write(content)


def get_page(text):
    global page_
    text = http_adder(text)
    response = requests.get(text)
    soup = BeautifulSoup(response.content, 'html.parser')
    page = soup.find_all('p')
    page = page + soup.find_all('a')
    page = page + soup.find_all('li')
    for tag in page:
        if tag.name == 'a':
            page_ = page_ + Fore.BLUE + tag.get_text() + Fore.RESET
        else:
            page_ = page_ + tag.get_text()
    return page_


while True:
    url = input().lower()

    if url == '':
        continue
    elif url == 'exit':
        break
    elif url == 'nytimescom':
        url = 'https://nytimes.com'
    elif url == 'bloombergcom':
        url = 'https://bloomberg.com'
    elif url == 'wiki':
        url = 'https://en.wikipedia.org'

    back_url = back_view(url)
    if back_url:
        #############################
        print(get_page(back_url))
        continue
        #############################

    tab_url = tab_view(url)
    if tab_url:
        #############################
        print(get_page(tab_url))
        continue
        #############################

    tab_save(url)

    url = http_adder(url)
    back_save(url)
    page_content = get_page(url)
    if page_content:
        print(page_content)
        name_of_file = file_name(url)
        file_save(page_content, direction_name, name_of_file)
        continue