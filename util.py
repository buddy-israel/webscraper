from bs4 import BeautifulSoup
import requests

s = requests.Session()


def send_request(url):
	try:
		r = s.get(url).text
		soup = BeautifulSoup(r, 'html.parser')
		return str(soup)
	except Exception:
		print("error on: send_request")
		return False


def save(file_path, contend):
	try:
		with open(file_path, 'w', encoding='utf-8') as outfile:
			outfile.write(contend)
	except Exception:
		return False


def open_file(file_path):
	try:
		with open(file_path, "r", encoding="utf-8") as fp:
			soup = BeautifulSoup(fp, 'html.parser')
			return soup
	except Exception:
		return False
