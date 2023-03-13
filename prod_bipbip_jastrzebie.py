#!/bin/bash
import gspread, requests, urllib3, bs4, os
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

jz_res_o = requests.get("https://bip.jastrzebie.pl/artykuly/zarzadzenia-1?page=1&limit=25")
jz_res_o.raise_for_status()
print("-----------------------------------------")
print("Połączono z zarządzeniami prezydenta.")

# Zarządzenia prezydenta
jz_soup_p = bs4.BeautifulSoup(jz_res_o.text, "html.parser")
jz_urls_soup_p = (jz_soup_p.find_all("table"))
jz_urls_p = []
for item in jz_urls_soup_p:
	jz_urls_p.append("https://bip.jastrzebie.pl/zarzadzenie/z-" + item.find('a', href=True).text.replace(".", "-"))

jz_dates_soup_p = (jz_soup_p.find_all("td"))
jz_dates_p = []
for item in jz_dates_soup_p[2::5]:
	jz_dates_p.append(item.text)
if sheet.acell('A4').value == jz_dates_p[0]:
	print("Brak nowych zarządzeń prezydenta!")

else:
	jz_body_p = []
	for item in jz_dates_soup_p[3::5]:
		jz_body_p.append(item.text)

	print("Aktualizuję zarządzenia prezydenta...")
	# Aktualizacja dat
	dates_cell_list_p = sheet.range("A4:A28")
	for j, cell in enumerate(dates_cell_list_p):
		cell.value = jz_dates_p[j]
	sheet.update_cells(dates_cell_list_p)
	# Aktualizacja treści
	body_cell_list_p = sheet.range("B4:B28")
	for j, cell in enumerate(body_cell_list_p):
		cell.value = jz_body_p[j]
	sheet.update_cells(body_cell_list_p)
	# Aktualizacja linków
	urls_cell_list_p = sheet.range("C4:C28")
	for j, cell in enumerate(urls_cell_list_p):
		cell.value = jz_urls_p[j]
	sheet.update_cells(urls_cell_list_p)
	print("Zarządzenia prezydenta zostały zaktualizowane!")
print("-----------------------------------------")

jz_res_rm = requests.get("https://bip.jastrzebie.pl/artykuly/uchwaly-2?page=1&limit=25")
jz_res_rm.raise_for_status()
print("Połączono z uchwałami rady miasta.")

# Uchwały rady miasta
jz_soup_rm = bs4.BeautifulSoup(jz_res_rm.text, "html.parser")

jz_dates_soup_rm = jz_soup_rm.find_all("td")
jz_dates_rm = []
for item in jz_dates_soup_rm:
	if item.text.endswith(".2023"):
		jz_dates_rm.append(item.text)
del jz_dates_rm[::2]

if sheet.acell('A32').value == jz_dates_rm[0]:
	print("Brak nowych uchwał rady miasta!")
else:
	jz_urls_soup_rm = (jz_soup_rm.find_all("table"))
	jz_urls_rm = []
	for item in jz_urls_soup_rm:
		jz_urls_rm.append("https://bip.jastrzebie.pl/uchwala/u-" + item.find('a', href=True).text.replace(".", "-"))
	jz_body_rm = []
	jz_body_soup_rm = jz_soup_rm.find_all('th', {'scope':'row'})
	for item in jz_body_soup_rm:
		if item.text == "W sprawie:":
			jz_body_rm.append(item.next_sibling.next_sibling.text)

	print("Aktualizuję uchwały rady miasta...")
	# Aktualizacja dat
	dates_cell_list_rm = sheet.range("A32:A56")
	for j, cell in enumerate(dates_cell_list_rm):
		cell.value = jz_dates_rm[j]
	sheet.update_cells(dates_cell_list_rm)
	# Aktualizacja treści
	body_cell_list_rm = sheet.range("B32:B56")
	for j, cell in enumerate(body_cell_list_rm):
		cell.value = jz_body_rm[j]
	sheet.update_cells(body_cell_list_rm)
	# Aktualizacja linków
	urls_cell_list_rm = sheet.range("C32:C56")
	for j, cell in enumerate(urls_cell_list_rm):
		cell.value = jz_urls_rm[j]
	sheet.update_cells(urls_cell_list_rm)
	print("Zarządzenia prezydenta zostały zaktualizowane!")
print("-----------------------------------------")

now = datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")
sheet.update('A1', f"Ostatnia aktualizacja: {date_time}")