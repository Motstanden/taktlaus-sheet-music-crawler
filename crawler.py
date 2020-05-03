import os
from dotenv import load_dotenv
from typing import Tuple, List
import requests
from bs4 import BeautifulSoup, element as bs4_element
import re
from pathlib import Path

class color:
    YELLOW = '\033[33m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    END = '\033[m' 

def header_print(text :str, header_color :color = color.YELLOW) -> None:
    print('\n')
    print(header_color + ':::::::::::::::::', text.upper(), ':::::::::::::::::', color.END)    

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
def create_valid_file_name(dirty_name :str, dirty_size :str):
    
    dirty_size = re.sub('\.',' dot ', dirty_size)   # replace . with dot
    clean_size = re.sub('\s','-', dirty_size)       # replace white space characters with -
    size = '____' + clean_size                            # prepend ____

    # Add the csize string before the file extension '.pdf' 
    dirty_name = re.sub('\.pdf', size, dirty_name)
    dirty_name += '.pdf'

    clean_name = re.sub('[<>:"/\|?*]', '', dirty_name)  # Remove characters that are not allowed by windows
    
    return clean_name

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
    
def run(print_progress = True):
    domain = 'https://taktlaus.no'
    username, password = setup_environment()
    
    session = login(username, password)

    archive_url = domain + '/sheetmusic'
    archive_table = find_table(archive_url, session)

    changed_folders =[] 
    counter = 0
    for row in archive_table:
        song_title, relative_url, arranger, composer = parse_table_row(row)
        # print('{:<60}'.format(title), '{:<20}'.format(url), '{:<30}'.format(arranger), '{:<30}'.format(composer))

        # Create a valid folder name
        folder_name = song_title + "____" + arranger + '____' + composer
        filtered_folder_name = re.sub('[<>:"/\|?*]', '', folder_name)
        # folder_path = Path('./downloads/'+ filtered_folder_name)
        folder_path = Path().joinpath('./downloads').joinpath(filtered_folder_name)
        song_url = domain + relative_url
        song_table = find_table(song_url, session)

        folder = song_folder()
        folder.path = folder_path.absolute()
        if folder_path.exists():
            # update folder
            folder.is_new = False

            for row in song_table:
                name, pdf_url, size_string = parse_song_table_row(row)      

                # Make a valid path
                file_name = create_valid_file_name(name, size_string)
                file_path = folder_path.joinpath(file_name)
                file_path = file_path.with_suffix('.pdf')

                if print_progress:
                    print('Checking if',color.YELLOW, name, color.END, 'is in', color.YELLOW, file_path, color.END)

                if not file_path.exists():
                    # Get the pdf from the url, and save it to the valid path
                    if print_progress:
                        print('Downloading ....... ', color.GREEN, name, color.END)

                    r = session.get(pdf_url)        
                    save_pdf(r.content, file_path)
                    folder.new_files.append(file_path.absolute())
                    
        else:
            # Create new folder and download everything from the song_table
            folder_path.mkdir()
            folder.is_new = True

            for row in song_table:
                name, pdf_url, size_string = parse_song_table_row(row)        
                
                if print_progress:
                    print('Downloading ....', color.GREEN, name, color.END)

                # Make a valid path
                file_name = create_valid_file_name(name, size_string)
                file_path = folder_path.joinpath(file_name)
                file_path = file_path.with_suffix('.pdf')

                # Get the pdf from the url, and save it to the valid path
                r = session.get(pdf_url)        
                save_pdf(r.content, file_path)
                folder.new_files.append(file_path.absolute())

        if folder.new_files:
            changed_folders.append(folder)

        # fast run through code for debug purposes 
        counter += 1
        if counter > 4:  
            return changed_folders
    print()
    print(color.GREEN, 'DONE', color.END)

class song_folder:

    def __init__(self):
        self.is_new = None
        self.path = None
        self.new_files = []


if __name__ == "__main__":
    os.system('cls')
    
    changed_folders = run()
    print('\n\n')   

    for folder in changed_folders:
        print('Folder is new:', folder.is_new)
        print('Folder path:  ', folder.path)
        
        print('New files:')
        for file in folder.new_files:
            print('                      ', file)
        
        print('\n \n')
