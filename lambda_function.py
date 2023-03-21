import urllib.request
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

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"} 

def fetch_data(url, headers):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"Error: {str(e)}")

url = str(f'https://api.bseindia.com/BseIndiaAPI/api/DwnldExcelIT15/w?scripcode=500180&fromdt={from_date}&todt={to_date}&flag=InsiderTrade15')
print(url)
data = fetch_data(url, headers)
if data:
    print(data.decode("utf-8"))