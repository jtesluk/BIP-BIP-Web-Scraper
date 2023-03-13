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

# Uchwały RM
mik_res_rm = requests.get("https://bip.mikolow.eu/?c=1171")
mik_res_rm.raise_for_status()
print("-----------------------------------------")
print("Połączono z uchwałami rady miasta.")
mik_soup_rm = bs4.BeautifulSoup(mik_res_rm.text, "html.parser")
mik_all_rm = mik_soup_rm.find_all(class_ = "blue")

mik_dates_rm = []
for item in mik_all_rm:
	linkus = "https://bip.mikolow.eu/" + item.get('href')
	mik_res_rm2 = requests.get(linkus)
	soup = bs4.BeautifulSoup(mik_res_rm2.content, "html.parser")
	mik_all_r2 = mik_soup_rm.find("table",{"class":"pretty"})
	tab = soup.find(id="specification").find("tr")
	mik_dates_rm.append(tab.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.next_element.next_sibling.text[0:10])

if sheet.acell("E4").value == mik_dates_rm[0]:
	print("Brak nowych uchwał rady miasta.")
else:
	mik_urls_rm = []
	for item in mik_all_rm:
		mik_urls_rm.append("https://bip.mikolow.eu/" + item.get('href'))
	mik_content_rm = []
	for item in mik_all_rm:
		count = item.text.find("w sprawie")
		mik_content_rm.append(item.text[count:])
	mik_all_r2 = mik_soup_rm.find_all("table", {"class" : "pretty"})

	print("Aktualizuję uchwały rady miasta...")
	# Aktualizacja dat
	documents_counter = len(mik_content_rm)
	dates_cell_list_rm = sheet.range(f"E4:E{documents_counter+3}")
	for j, cell in enumerate(dates_cell_list_rm):
		cell.value = mik_dates_rm[j]
	sheet.update_cells(dates_cell_list_rm)
	# Aktualizacja treści
	content_cell_list_rm = sheet.range(f"F4:F{documents_counter+3}")
	for j, cell in enumerate(content_cell_list_rm):
		cell.value = mik_content_rm[j]
	sheet.update_cells(content_cell_list_rm)
	# Aktualizacja linków
	urls_cell_list_rm = sheet.range(f"G4:G{documents_counter+3}")
	for j, cell in enumerate(urls_cell_list_rm):
		cell.value = mik_urls_rm[j]
	sheet.update_cells(urls_cell_list_rm)
	print("Uchwały rady miasta zostały zaktualizowane!")
print("-----------------------------------------")

# Zarządzenia burmistrza
mik_res_p = requests.get("https://bip.mikolow.eu/?c=1173")
mik_res_p.raise_for_status()
print("Połączono z zarządzeniami burmistrza.")
mik_soup_p = bs4.BeautifulSoup(mik_res_p.content, "html.parser")
mik_all_p = mik_soup_p.find_all(class_ = "blue")

mik_dates_p = []
for item in mik_all_p:
	linkusp = "https://bip.mikolow.eu/" + item.get('href')
	mik_res_p2 = requests.get(linkusp)
	soup = bs4.BeautifulSoup(mik_res_p2.content, "html.parser")
	mik_all_p2 = mik_soup_p.find("table",{"class":"pretty"})
	tab = soup.find(id="specification").find("tr")
	mik_dates_p.append(tab.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.next_element.next_sibling.text[0:10])

if sheet.acell("A4").value == mik_dates_p[0]:
	print("Brak nowych uchwał rady miasta")
else:
	mik_urls_p = []
	for item in mik_all_p:
		mik_urls_p.append("https://bip.mikolow.eu/" + item.get('href'))
	mik_content_p = []
	for item in mik_all_p:
		count = item.text.find("w sprawie")
		mik_content_p.append(item.text[count:])
	mik_all_p2 = mik_soup_p.find_all("table", {"class" : "pretty"})

	print("Aktualizuję zarządzenia burmistrza...")
	# Aktualizacja dat
	dates_cell_list_p = sheet.range(f"A4:A28")
	for j, cell in enumerate(dates_cell_list_p):
		cell.value = mik_dates_p[j]
	sheet.update_cells(dates_cell_list_p)
	# Aktualizacja treści
	content_cell_list_p = sheet.range(f"B4:B28")
	for j, cell in enumerate(content_cell_list_p):
		cell.value = mik_content_p[j]
	sheet.update_cells(content_cell_list_p)
	# Aktualizacja linków
	urls_cell_list_p = sheet.range(f"C4:C28")
	for j, cell in enumerate(urls_cell_list_p):
		cell.value = mik_urls_p[j]
	sheet.update_cells(urls_cell_list_p)
	print("Zarządzenia burmistrza zostały zaktualizowane!")
print("-----------------------------------------")


now = datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")
sheet.update('A1', f"Ostatnia aktualizacja: {date_time}")
