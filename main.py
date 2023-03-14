import requests

def get_insider_data(company):
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
  r = requests.get(f'https://api.bseindia.com/BseIndiaAPI/api/DwnldExcelIT15/w?scripcode={company}&fromdt=&todt=&flag=InsiderTrade15', headers=headers)
  print(r.text)

get_insider_data(500510)