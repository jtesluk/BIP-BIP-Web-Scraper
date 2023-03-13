#!/usr/bin/python3
import gspread, requests, urllib3, os, bs4
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

scopes = [
	'https://www.googleapis.com/auth/spreadsheets',
	'https://www.googleapis.com/auth/drive'
]
path = os.getcwd()
credentials_path = os.path.join(path, "credentials_file_name")

creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes = scopes)
file = gspread.authorize(creds)
workbook = file.open_by_key('XXXXXX WORKBOOK KEY XXXXXXX')
sheet = workbook.worksheet('WORKSHEET NAME')



# Ogłoszenia urzędowe
rbk_res_o = requests.get("https://bip.um.rybnik.eu/Default.aspx?Page=31")
rbk_res_o.raise_for_status()
print("-----------------------------------------")
print("Połączono z ogłoszeniami urzędowymi.")
rbk_soup_o = bs4.BeautifulSoup(rbk_res_o.text, "html.parser")
rbk_date_o = []
rbk_date_o_all = rbk_soup_o.find_all("td", class_="text-nowrap text-center") # Wyszukiwanie dat ogłoszeń
for item in rbk_date_o_all:
	rbk_date_o.append(item.text)
#Jeśli najnowsza data w arkuszu i w BIPie jes ta sama, oznacza to brak nowych ogłoszeń i można przejsć dalej.
if sheet.acell('A4').value == rbk_date_o_all[0].text:
	print("Brak nowych ogłoszeń urzędowych!")


# Jeśli znaleziono nowe ogłoszenia, skrypt się uruchamia.
else:
	print("Znaleziono nowe ogłoszenia urzędowe w Rybniku.")
	rbk_url_o = rbk_soup_o.find_all("a", class_="btn btn-primary") # Wyszukiwanie linków do ogłoszeniach
	rbk_url_pre_o = "https://bip.um.rybnik.eu/"
	rbk_urls_o = []
	for url in rbk_url_o:
		rbk_url_post = rbk_url_pre_o+url.get("href")
		rbk_urls_o.append(rbk_url_post) # Wydobycie linków i wrzucenie ich do listy, z której zostaną wrzucone do arkusza
	rbk_body_o = []
	for i in range(0, 50):
		rbk_body_o.append(rbk_date_o_all[i].nextSibling.nextSibling.text) # Wydobycie treści ogłoszeń i wrzucenie do listy


	print("Aktualizuję ogłoszenia urzędowe...")
	# Aktualizacja linków
	urls_cell_list_o = sheet.range("C4:C28")
	for j, cell in enumerate(urls_cell_list_o):
		cell.value = rbk_urls_o[j]
	sheet.update_cells(urls_cell_list_o)
	# Aktualizacja dat
	dates_cell_list_o = sheet.range("A4:A28")
	for j, cell in enumerate(dates_cell_list_o):
		cell.value = rbk_date_o[j]
	sheet.update_cells(dates_cell_list_o)
	# Aktualizacja treści
	body_cell_list_o = sheet.range("B4:B28")
	for j, cell in enumerate(body_cell_list_o):
		cell.value = rbk_body_o[j]
	sheet.update_cells(body_cell_list_o)

	print("Ogłoszenia urzędowe zostały zaktualizowane!\n")
print("-----------------------------------------")

# Zarządzenia prezydenta
rbk_res_p = requests.get("https://bip.um.rybnik.eu/Default.aspx?Page=214")
rbk_res_p.raise_for_status()
print("Połączono z zarządzeniami prezydenta.")
rbk_soup_p = bs4.BeautifulSoup(rbk_res_p.text, "html.parser")
rbk_date_p_all = rbk_soup_p.find_all("td", class_="text-nowrap text-center")
rbk_date_p = []
for item in rbk_date_p_all:
	rbk_date_p.append(item.text)
if sheet.acell('E4').value == rbk_date_p[0]:
	print("Brak nowych zarządzeń prezydenta!")
else:
	table_body_p = rbk_soup_p.find_all("tbody")
	rbk_url_p = rbk_soup_p.find_all("a", class_="btn btn-primary")
	rbk_url_pre_p = "https://bip.um.rybnik.eu/"
	rbk_urls_p = []
	for url in rbk_url_p:
		rbk_url_post_p = rbk_url_pre_p+url.get("href")
		rbk_urls_p.append(rbk_url_post_p)
	rbk_body_p = []
	for i in range(0, 25):
		rbk_body_p.append(rbk_date_p_all[i].previousSibling.previousSibling.text)

	print("Aktualizuję zarządzenia prezydenta...")

	# Aktualizacja linków
	urls_cell_list_p = sheet.range("G4:G28")
	for j, cell in enumerate(urls_cell_list_p):
		cell.value = rbk_urls_p[j]
	sheet.update_cells(urls_cell_list_p)
	# Aktualizacja dat
	dates_cell_list_p = sheet.range("E4:E28")
	for j, cell in enumerate(dates_cell_list_p):
		cell.value = rbk_date_p[j]
	sheet.update_cells(dates_cell_list_p)
	# Aktualizacja treści
	body_cell_list_p = sheet.range("F4:F28")
	for j, cell in enumerate(body_cell_list_p):
		cell.value = rbk_body_p[j]
	sheet.update_cells(body_cell_list_p)

	print("Zarządzenia prezydenta zostały zaktualizowane!")
print("-----------------------------------------")

# Uchwały RM
rbk_res_rm = requests.get("https://bip.um.rybnik.eu/Default.aspx?Page=247")
rbk_res_rm.raise_for_status()
print("Połączono z uchwałami rady miasta.")
rbk_soup_rm = bs4.BeautifulSoup(rbk_res_rm.text, "html.parser")
rbk_date_rm_all = rbk_soup_rm.find_all("td", class_="text-nowrap text-center")
rbk_date_rm = []
for item in rbk_date_rm_all:
	rbk_date_rm.append(item.text)
if sheet.acell('A32').value == rbk_date_rm[0]:
	print("Brak nowych uchwał rady miasta!\n")
else:
	rbk_url_rm = rbk_soup_rm.find_all("a", class_="btn btn-primary")
	rbk_url_pre_rm = "https://bip.um.rybnik.eu/"
	rbk_urls_rm = []
	for url in rbk_url_rm:
		rbk_url_post_rm = rbk_url_pre_rm+url.get("href")
		rbk_urls_rm.append(rbk_url_post_rm)
	rbk_body_rm = []
	for i in range(0, 50):
		rbk_body_rm.append(rbk_date_rm_all[i].nextSibling.nextSibling.text)


	print("Aktualizuję uchwały rady miasta...") # Aktualizacja uchwał w arkuszu

	# Aktualizacja linków
	urls_cell_list_rm = sheet.range("C32:C56")
	for j, cell in enumerate(urls_cell_list_rm):
		cell.value = rbk_urls_rm[j]
	sheet.update_cells(urls_cell_list_rm)
	# Aktualizacja dat
	dates_cell_list_p = sheet.range("A32:A56")
	for j, cell in enumerate(dates_cell_list_p):
		cell.value = rbk_date_rm[j]
	sheet.update_cells(dates_cell_list_p)
	# Aktualizacja treści
	body_cell_list_rm = sheet.range("B32:B56")
	for j, cell in enumerate(body_cell_list_rm):
		cell.value = rbk_body_rm[j]
	sheet.update_cells(body_cell_list_rm)

	print("Uchwały rady miasta zostały zaktualizowane.")

now = datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")
sheet.update('A1', f"Ostatnia aktualizacja: {date_time}")
