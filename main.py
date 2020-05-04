import os
import crawler
from typing import List
from pathlib import Path
import re
from string import Template
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def clear_terminal():
    os.system('clear')

def build_email_body(folders :List[ crawler.song_folder]) -> str:

    col1_width = 20
    col2_width = 20
    body = ""
    for folder in folders:

        song_title, arranger, composer = re.split('____', folder.path.name)

        body += '\n'
        body += 'New song: ' if folder.is_new else 'This song has new files: ' 
        body += '\n\tSong: ' + song_title

        if arranger.strip() != '':
            body += '\n\tArranger: ' + arranger

        if composer.strip() != '':
            body += '\n\tComposer: ' + composer

        for file in folder.new_files:
            file_name, dirty_size = re.split('____', file.name)

            dirty_size = re.sub('-dot-', '.', dirty_size)
            size = re.sub('-', ' ', dirty_size)

            body += '\n'
            body += '\t\tNew file:\t' + file_name + '\t\t\tsize:\t' + size 

        body += '\n'
        body += '----------------------------------------------------------------------------------------------------------------------------------------'
    return body

# Read a .txt file as a template string
def read_template(path :str):
    with open(path, 'r') as file:
        return Template(file.read())

# Get every line in .txt file, and return them as a list of strings
def get_mail_list() -> List[str]:
    emails = [] 
    with open('mailing-list.txt', 'r') as file:
        for line in file:
            email = line.strip()
            emails.append(email)
    return emails

def send_emails(body :str) -> None:

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:

        # Get credentials from .env file
        username = os.getenv('EMAIL_USERNAME')
        password = os.getenv('EMAIL_PASSWORD')

        # Login to email account
        server.ehlo()
        server.login(username, password)
        
        mail_list = get_mail_list()
        for mail_address in mail_list:
            # Todo: experiment with the mime types
            msg = MIMEMultipart()           # Mail
            msg['From'] = username          # From this email user
            msg['To'] = mail_address        # To this address
            msg['Subject'] = 'Nye noter er tilgjengelig'  # With this tile 
            msg.attach(MIMEText(body))   # With this text body

            server.send_message(msg)

def start_crawl():
    load_dotenv()
    changed_folders = crawler.run()  

    # if anythig has changed:
    if len(changed_folders) > 0:
        body = build_email_body(changed_folders)
        print(body)        

        template = read_template('./template-mail.txt')
        full_message = template.substitute(BODY=body)
        send_emails(full_message)

if __name__ == "__main__":
    clear_terminal()
    start_crawl()

