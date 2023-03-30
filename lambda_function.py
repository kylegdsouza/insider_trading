import os
from datetime import date
import requests
import pandas as pd
from io import StringIO

# Check Insider trades only for TODAY
to_date = date.today().strftime('%d/%m/%Y')
from_date = to_date

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

df = pd.DataFrame()

def get_insider_data(to_date, from_date):
  url = f'https://api.bseindia.com/BseIndiaAPI/api/DwnldExcelIT15/w?scripcode=&fromdt={from_date}&todt={to_date}&flag=InsiderTrade15'
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


data = get_insider_data(to_date, from_date)
if data:
  df = df.append(create_dataframe_from_csv(data))
  
print(df.info())
market_purchase = df.loc[df['Mode of Acquisition'] == 'Market Purchase']
def unit_lakhs(x):
  return round(x/100000,2)

summed = market_purchase.groupby('Security Name')['Value  of Securities Acquired/Disposed/Pledge etc'].sum()
sorted_summed = summed.sort_values(ascending=False)
lakhs_summed = sorted_summed.apply(unit_lakhs)

send_telegram_message(lakhs_summed)