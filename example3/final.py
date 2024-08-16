import json
from bs4 import BeautifulSoup

with open('test.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

html_content = data[0]['table']

soup = BeautifulSoup(html_content, 'html.parser')

parsed_data = []
table = soup.find('table')
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
    year = cols[0].text
    for month_index, month_name in enumerate(months.keys()):
        rate = cols[month_index + 1].text.strip()
        if rate:
            parsed_data.append((year, months[month_name], rate))


with open('output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(f"{'YIL':<5} {'AY':<5} {'DEGER':<10}\n")
    output_file.write("-" * 25 + "\n")
    for entry in parsed_data:
        output_file.write(f"{entry[0]:<5} {entry[1]:<5} {entry[2]:<10}\n")

print("Veriler 'output.txt' dosyasına yazıldı.")