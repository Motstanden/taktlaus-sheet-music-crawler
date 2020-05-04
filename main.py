import os
import crawler
from typing import List
from pathlib import Path
import re

def clear_terminal():
    os.system('clear')

def build_email_body(folders :List[ crawler.song_folder]) -> str:

    col1_width = 20
    col2_width = 20
    body = ""
    for folder in folders:

        song_title, arranger, composer = re.split('____', folder.path.name)

        body += '\n\n'
        body += 'New song: ' if folder.is_new else 'This song has new files: ' 
        body += '{0: <50}'.format('\n\tSong: ' + song_title)

        if arranger.strip() != '':
            body += '{0: <50}'.format('Arranger: ' + arranger)

        if composer.split() != '':
            body += '{0: <50}'.format('Composer: ' + composer)

        for file in folder.new_files:
            file_name, dirty_size = re.split('____', file.name)

            dirty_size = re.sub('-dot-', '.', dirty_size)
            size = re.sub('-', ' ', dirty_size)
            
            body += '{0: <75}'.format('\n\t\tNew file:\t' + file_name) 
            body += '{0: <50}'.format('\tsize:\t' + size)

    return body


def send_emails(body :str) -> None:
    pass

def start_crawl():
    changed_folders = crawler.run()  

    # if anythig has changed:
    if len(changed_folders) > 0:
        body = build_email_body(changed_folders)
        send_emails(body)



if __name__ == "__main__":
    clear_terminal()
    start_crawl()

