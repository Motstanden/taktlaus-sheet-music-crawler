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

def save_pdf(file :bytes, path):
    with open(path, 'wb') as f:
        f.write(file)

def login(username :str, password :str) -> requests.sessions.Session:
    # In order to stay logged in we must start a session
    session = requests.session()
    # Credentials that must be sent 
    data = {
        'name': username,
        'pass': password,
        'form_build_id': 'form-s_5qMqZ0hgv3ZOpDLDntan3HODbAxRoFeIqaW2f0hJk',
        'form_id': 'user_login_block',
        'antibot_key': '2d1379116de05898e27d9033859db912',
        'op': 'Logg+inn'
    }
    url = 'https://taktlaus.no/node/2?destination=node/6225' # login url
    r = session.post(url, data=data) # Perform a login action

    return session 

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

def find_table(url :str, session :requests.sessions.Session) -> bs4_element.Tag:
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.select('tbody tr')

    return table

if __name__ == "__main__":
    clear_terminal()

    domain = 'https://taktlaus.no'
    username, password = setup_environment()
    
    session = login(username, password)

    archive_url = domain + '/sheetmusic'
    archive_table = find_table(archive_url, session)

    for row in archive_table:
        song_title, relative_url, arranger, composer = parse_table_row(row)
        # print('{:<60}'.format(title), '{:<20}'.format(url), '{:<30}'.format(arranger), '{:<30}'.format(composer))

        if song_title == '99 Luftballons': 
            
            song_url = domain + relative_url
            song_table = find_table(song_url, session)
            
            for row in song_table:
                name, pdf_url, size_string = parse_song_table_row(row)
            
            print('{:<40}'.format(name), '{:<100}'.format(pdf_url), '{:<20}'.format(size_string))
            
            r = session.get(pdf_url)
            path = './downloads/' + name
            save_pdf(r.content, path)

            break # work in progress

# def download_pdf(s )
