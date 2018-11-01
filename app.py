from datetime import datetime
from os import listdir, remove, environ, path, makedirs
from pathlib import Path
from shutil import copy2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# e-mail configuration
SENDER_LOGIN = environ.get('SUSER')
SENDER_PASS = environ.get('SPASS')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
RECIPIENT_EMAIL = environ.get('DMAIL')
BACKUP_FILES_COUNT = 30

# backup configuration
SRC_FILE = 'testfile.zip'  # database file name
DST_DIR = 'backup'  # folder name
DAY_SEND_TO_EMAIL = 5

BASE_DIR = str(Path().absolute())
BCK_DIR = f'{BASE_DIR}/{DST_DIR}'
if not path.exists(BCK_DIR):
	makedirs(BCK_DIR)
DT = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
FILES = listdir(f'{BASE_DIR}/{DST_DIR}')
DATE = datetime.today().strftime('%d/%m/%Y')
WEEKDAY = datetime.isoweekday(datetime.today())


def copy_file():
	copy2(f'{BASE_DIR}/{SRC_FILE}', f'{BASE_DIR}/{DST_DIR}/{DT}_{SRC_FILE}')


def remove_last_file():
	files_count = len(FILES)
	if files_count > 0:
		FILES.sort()
		last_item = FILES[0]
		if files_count == BACKUP_FILES_COUNT:
			remove(f'{BASE_DIR}/{DST_DIR}/{last_item}')


def get_last_copied_file():
	last_file = listdir(f'{BASE_DIR}/{DST_DIR}')
	last_file.sort()
	return last_file[-1]


def send_file_to_email():
	msg_subject = f'KeePass Backup from day: {DATE}'
	msg = MIMEMultipart()
	msg['From'] = SENDER_LOGIN
	msg['To'] = RECIPIENT_EMAIL
	msg['Subject'] = msg_subject
	body = f'KeePass Backup from day: {DATE}'

	msg.attach(MIMEText(body, 'plain'))

	file_name = get_last_copied_file()
	attachment = open(f'{BASE_DIR}/{DST_DIR}/{file_name}', 'rb')

	part = MIMEBase('application', 'octet-stream')
	part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', f'attachment; filename= {file_name}')

	msg.attach(part)

	server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	server.starttls()
	server.login(SENDER_LOGIN, SENDER_PASS)
	text = msg.as_string()
	server.sendmail(SENDER_LOGIN, RECIPIENT_EMAIL, text)
	server.quit()


def main():
	copy_file()
	remove_last_file()
	if WEEKDAY == DAY_SEND_TO_EMAIL:
		try:
			send_file_to_email()
		except Exception as ex:
			print(ex)


if __name__ == '__main__':
	main()


