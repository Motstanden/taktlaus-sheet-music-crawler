import os
from dotenv import load_dotenv
from typing import Tuple
import requests
from bs4 import BeautifulSoup, element as bs4_element
import re

class color:
    YELLOW = '\033[33m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    END = '\033[m' 

def header_print(text :str, header_color :color = color.YELLOW) -> None:
    print('\n')
    print(header_color + ':::::::::::::::::', text.upper(), ':::::::::::::::::', color.END)    

def clear_terminal():
    os.system('clear')

def parse_table_row(row :bs4_element.Tag) -> Tuple[str, str, str, str]:
    # Find the anchor that contains the name of the song, and the url to the song pdfs
    anchor = row.find('a')
    title = anchor.string.strip()
    url = anchor['href'].strip()

    # Use regex to find the column that holds the arranger info. 
    arranger_tag = row.find(attrs=re.compile('arranger'))
    arranger = arranger_tag.string.strip()

    # ... and do the same for the composer
    composer_tag = row.find(attrs=re.compile('composer'))
    composer = composer_tag.string.strip()

    return title, url, arranger, composer 

def parse_song_table_row(row :bs4_element.Tag) -> Tuple[str, str, str]:

    # Find the anchor that contains the name of the song, and the url to the pdf
    anchor = row.find('a')
    name = anchor.string.strip()
    url = anchor['href'].strip()

    # Finds a column that contains the size string 
    columns = row.find_all('td')
    size = columns[1].string.strip()

    return name, url, size 

def setup_environment() -> Tuple[str, str]:
    load_dotenv()
    username = os.getenv('TAKTLAUS_USERNAME')
    password = os.getenv('TAKTLAUS_PASSWORD')
    return username, password 

if __name__ == "__main__":
    clear_terminal()
    username, password = setup_environment()

    s = requests.session()
    domain = 'https://taktlaus.no'
    data = {
        'name': username,
        'pass': password,
        'form_build_id': 'form-s_5qMqZ0hgv3ZOpDLDntan3HODbAxRoFeIqaW2f0hJk',
        'form_id': 'user_login_block',
        'antibot_key': '2d1379116de05898e27d9033859db912',
        'op': 'Logg+inn'
    }
    url = 'https://taktlaus.no/node/2?destination=node/6225'
    r = s.post(url, data=data)
    print(r)

    soup = BeautifulSoup(r.content, 'lxml')   

    url2 = 'https://taktlaus.no/sheetmusic'
    r2 = s.get(url2)
    soup2 = BeautifulSoup(r2.content, 'lxml')

    table = soup2.select('tbody tr')

    for row in table:
        title, url, arranger, composer = parse_table_row(row)
        # print('{:<60}'.format(title), '{:<20}'.format(url), '{:<30}'.format(arranger), '{:<30}'.format(composer))
        if title == '99 Luftballons': 
            break # Work in progres, this will be removed once finished


    song_url = domain + url
    r3 = s.get(song_url)
    soup3 = BeautifulSoup(r3.content, 'lxml')

    table = soup3.select('tbody tr')
    for row in table:
        name, pdf_url, size_string = parse_song_table_row(row)
        print('{:<40}'.format(name), '{:<100}'.format(pdf_url), '{:<20}'.format(size_string))
    