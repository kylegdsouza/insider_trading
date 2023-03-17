import requests
from datetime import date
import csv

# Make a list of security codes of BSE group stocks
security_codes = []
with open('data/EQ170323.CSV', 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)
  for row in reader:
    if row[2] == 'A ':
      security_codes.append(row[0])
    else:
      continue

# Check Insider trades only for TODAY
to_date = date.today().strftime('%d/%m/%Y')
from_date = to_date


def get_insider_data(company):
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"} 
  response = requests.get(f'https://api.bseindia.com/BseIndiaAPI/api/DwnldExcelIT15/w?scripcode={company}&fromdt={from_date}&todt={to_date}&flag=InsiderTrade15', headers=headers)
  if response.status_code == 200:
    lines = response.content.decode('utf-8').splitlines()
    if not lines:
      print(f"{company} No Transaction")
    else:
      lines.pop(0)
      # Write the response content to a CSV file
      with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Decode the response content as text and write each row to the CSV file
        for row in lines:
          print(row)
          writer.writerow(row.split(','))
      print('CSV file saved successfully.')

for i in security_codes:
  get_insider_data(i)