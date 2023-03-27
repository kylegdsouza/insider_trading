import os
from datetime import date
import requests
import pandas as pd
from io import StringIO
import csv

# Make a list of security codes of BSE group stocks
security_codes = ['500003','500085','500265','500331','500510','505283','506943','508869','509480','512070','512179','512237','512455','513262','523405','531162','532187','532504','532523','532539','532683','532892','532927','533326','541403','542651']
# with open('data/EQ170323.CSV', 'r') as csvfile:
#   reader = csv.reader(csvfile)
#   next(reader)
#   for row in reader:
#     if row[2] == 'A ':
#       security_codes.append(row[0])
#     else:
#       continue

# Check Insider trades only for TODAY
to_date = date.today().strftime('%d/%m/%Y')
from_date = to_date
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
df = pd.DataFrame()

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
  
def create_dataframe_from_csv(csv_data):
  csv_data_io = StringIO(csv_data)
  df = pd.read_csv(csv_data_io)
  return df

for security_code in security_codes:
  data = get_insider_data(security_code, to_date, from_date)
  if data:
    df = df.append(create_dataframe_from_csv(data))

print(df.info())
market_purchase = df.loc[df['Mode of Acquisition'] == 'Market Purchase']

summed = market_purchase.groupby('Security Name')['Value  of Securities Acquired/Disposed/Pledge etc'].sum()

send_telegram_message(str(summed))