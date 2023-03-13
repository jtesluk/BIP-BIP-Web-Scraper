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


# Zarządzenia prezydenta
kat_res_o = requests.get("https://bip.katowice.eu/Ogloszenia/Zarzadzenia/zarzadzenia.aspx?menu=600&menu=600")
kat_res_o.raise_for_status()
print("-------------------------------------")
print("Połączono z zarządzeniami prezydenta.")
kat_soup_p = bs4.BeautifulSoup(kat_res_o.text, "html.parser")
kat_nr_p = []
for item in kat_soup_p.find_all("div", {"class": "col-md-2"}):
	kat_nr_p.append(item.text)
if sheet.acell('E4').value == kat_nr_p[1]:
	print("Brak nowych zarządzeń prezydenta.")
else:
	kat_urls_soup_p = kat_soup_p.find("div", {"class": "col-md-9 podstrona"})
	kat_urls_p = []
	for item in kat_urls_soup_p.find_all("a"):
		kat_urls_p.append("https://bip.katowice.eu/Ogloszenia/Zarzadzenia/" + item.get('href'))
	kat_body_p = []
	for item in kat_soup_p.find_all("h4"):
		kat_body_p.append(item.text.strip())

	# Aktualizacja numerów
	dates_cell_list_p = sheet.range("E4:E28")
	for j, cell in enumerate(dates_cell_list_p):
		cell.value = kat_nr_p[j+1]
	sheet.update_cells(dates_cell_list_p)
	# Aktualizacja treści
	body_cell_list_p = sheet.range("F4:F28")
	for j, cell in enumerate(body_cell_list_p):
		cell.value = kat_body_p[j]
	sheet.update_cells(body_cell_list_p)
	# Aktualizacja linków
	urls_cell_list_p = sheet.range("G4:G28")
	for j, cell in enumerate(urls_cell_list_p):
		cell.value = kat_urls_p[j+1]
	sheet.update_cells(urls_cell_list_p)
	print("Zaktualizowano zarządzenia prezydenta!")
print("-------------------------------------")
# Uchwały rady miasta
kat_res_all_rm = requests.get("https://bip.katowice.eu/RadaMiasta/Uchwaly/uchwalone_ses.aspx?menu=660&menu=660")
kat_res_all_rm.raise_for_status()
print("Połączono z uchwałami rady miasta.")
kat_last_url_all_rm = bs4.BeautifulSoup(kat_res_all_rm.text, "html.parser")
kat_last_url_rm = "https://bip.katowice.eu/RadaMiasta/Uchwaly/" + kat_last_url_all_rm.find("div", {"class":"panel-body"}).find("div",{"class":"col-md-2"}).find("a")["href"]
kat_res_rm = requests.get(kat_last_url_rm)
kat_res_rm.raise_for_status()
kat_date_rm_soup_rm = bs4.BeautifulSoup(kat_res_rm.text, "html.parser")
kat_date_rm = kat_date_rm_soup_rm.find_all("div", {"class": "tekstboks"})
kat_body_rm = []
kat_urls_rm = []
kat_dates_rm = []
for item in kat_date_rm:
	kat_dates_rm.append(item.contents[0].strip("\r\n\t\t\t\t\tData: "))
	for url in item.find_all("a"):
		kat_urls_rm.append("https://bip.katowice.eu/RadaMiasta/Uchwaly/" + url["href"])
		kat_body_rm.append(url.text)
documents_counter = len(kat_body_rm)

if sheet.acell('A4').value == kat_dates_rm[1]:
	print("Brak nowych uchwał rady miasta.")

else:
	# Aktualizacja dat
	dates_cell_list_rm = sheet.range(f"A4:A{documents_counter+3}")
	for j, cell in enumerate(dates_cell_list_rm):
		cell.value = kat_dates_rm[j]
	sheet.update_cells(dates_cell_list_rm)
	# Aktualizacja treści
	body_cell_list_rm = sheet.range(f"B4:B{documents_counter+3}")
	for j, cell in enumerate(body_cell_list_rm):
		cell.value = kat_body_rm[j]
	sheet.update_cells(body_cell_list_rm)
	# Aktualizacja linków
	urls_cell_list_rm = sheet.range(f"C4:C{documents_counter+3}")
	for j, cell in enumerate(urls_cell_list_rm):
		cell.value = kat_urls_rm[j]
	sheet.update_cells(urls_cell_list_rm)
	print("Uchwały rady miasta zostały zaktualizowane.")
now = datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")
sheet.update('A1', f"Ostatnia aktualizacja: {date_time}")
