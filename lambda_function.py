import os
from datetime import date
import requests

# Make a list of security codes of BSE group stocks
security_codes = ['531489']
# with open('data/EQ170323.CSV', 'r') as csvfile:
#   reader = csv.reader(csvfile)
#   next(reader)
#   for row in reader:
#     if row[2] == 'A ':
#       security_codes.append(row[0])
#     else:
#       continue

# Check Insider trades only for TODAY
to_date = '25/03/2023'
from_date = to_date
# to_date = date.today().strftime('%d/%m/%Y')
# from_date = to_date
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def get_insider_data(security_code, to_date, from_date):
  url = f'https://api.bseindia.com/BseIndiaAPI/api/DwnldExcelIT15/w?scripcode={security_code}&fromdt={from_date}&todt={to_date}&flag=InsiderTrade15'
  print(url)
  data = requests.get(url, headers=headers)
  return data.text

def send_telegram_message(message):
  telegram_token = os.environ['telegram_token']
  telegram_chat_id = os.environ['telegram_chat_id']
  url = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={message}'
  print(url)
  get_request = requests.get(url)
  return get_request.status_code
  
for security_code in security_codes:
  data = get_insider_data(security_code, to_date, from_date)
  if data:
    send_telegram_message(data)