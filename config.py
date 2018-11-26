from datetime import datetime
from os import listdir, environ, path, makedirs
from pathlib import Path

# e-mail configuration
SENDER_LOGIN = environ.get('SUSER')  # sender e-mail address (login)
SENDER_PASS = environ.get('SPASS')  # sender password
SMTP_SERVER = 'smtp.gmail.com'  # sender smtp server
SMTP_PORT = 587  # sender smtp port
RECIPIENT_EMAIL = environ.get('DMAIL')  # recipient email address
BACKUP_FILES_COUNT = 10  # number of backups

# backup configuration
SRC_FILE = 'database.kdbx'  # database file name
DST_DIR = 'backup'  # backup folder name
DAY_SEND_TO_EMAIL = 5  # the day of the week in which the backup will be sent to the email address

BASE_DIR = str(Path().absolute())
BCK_DIR = f'{BASE_DIR}/{DST_DIR}'
FILES = listdir(f'{BASE_DIR}/{DST_DIR}')
if not path.exists(BCK_DIR):
	makedirs(BCK_DIR)
DTN = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
DATE = datetime.today().strftime('%d/%m/%Y')
WEEKDAY = datetime.isoweekday(datetime.today())
