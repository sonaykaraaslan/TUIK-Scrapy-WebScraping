import requests
from bs4 import BeautifulSoup

url = 'https://www.hakedis.org/endeksler/tuketici-fiyat-genel-endeksi-ve-degisim-oranlari-2003'  # Buraya hedef URL'yi girin

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

parsed_data = []
table = soup.find('table', {'class': 'table table-striped table-bordered responsive'})
rows = table.find_all('tr')

months = {
    'OCAK': 1,
    'ŞUBAT': 2,
    'MART': 3,
    'NİSAN': 4,
    'MAYIS': 5,
    'HAZİRAN': 6,
    'TEMMUZ': 7,
    'AĞUSTOS': 8,
    'EYLÜL': 9,
    'EKİM': 10,
    'KASIM': 11,
    'ARALIK': 12
}

for row in rows[1:]:
    cols = row.find_all('td')
    year = int(cols[0].text)
    formatted_year = f"{year:,}".replace(".", ",")  
    for month_index, month_name in enumerate(months.keys()):
        rate = cols[month_index + 1].text.strip().replace('.', '').replace(',', '.')
        if rate:
            rate = float(rate)
            formatted_rate = f"{rate:,.2f}".replace(".", "X").replace(".", ",").replace("X", ".")  
            parsed_data.append((formatted_year, months[month_name], formatted_rate))

with open('output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(f"{'YIL':<8} {'AY':<5} {'DEGER':<10}\n")
    output_file.write("-" * 25 + "\n")
    for entry in parsed_data:
        output_file.write(f"{entry[0]:<8} {entry[1]:<5} {entry[2]:<10}\n")

print("Veriler 'output.txt' dosyasına yazıldı.")
