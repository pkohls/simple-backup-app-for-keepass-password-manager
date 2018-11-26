from utils import *


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
