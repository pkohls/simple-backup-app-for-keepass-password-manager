import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import remove
from shutil import copy2

from config import *


def copy_file():
	try:
		copy2(f'{BASE_DIR}/{SRC_FILE}', f'{BASE_DIR}/{DST_DIR}/{DTN}_{SRC_FILE}')
	except Exception as ex:
		print(ex)


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
