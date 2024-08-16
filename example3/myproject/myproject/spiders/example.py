# example_project/example_project/spiders/example_spider.py

import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["hakedis.org"]
    start_urls = [
        "https://www.hakedis.org/endeksler/tuketici-fiyat-genel-endeksi-ve-degisim-oranlari-2003"
    ]

    def parse(self, response):
        parsed_data = []
        months = {
            'OCAK': 1, 'ŞUBAT': 2, 'MART': 3, 'NİSAN': 4, 'MAYIS': 5, 'HAZİRAN': 6,
            'TEMMUZ': 7, 'AĞUSTOS': 8, 'EYLÜL': 9, 'EKİM': 10, 'KASIM': 11, 'ARALIK': 12
        }

        table = response.xpath('//table[@class="table table-striped table-bordered responsive"]')
        rows = table.xpath('.//tr')

        for row in rows[1:]:
            cols = row.xpath('.//td')
            year = cols[0].xpath('.//text()').get()
            formatted_year = f"{int(year):,}".replace(".", ",")
            for month_index, month_name in enumerate(months.keys()):
                rate = cols[month_index + 1].xpath('.//text()').get().strip().replace('.', '').replace(',', '.')
                if rate:
                    rate = float(rate)
                    formatted_rate = f"{rate:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
                    parsed_data.append(f"{formatted_year:<8} {months[month_name]:<5} {formatted_rate:<10}\n")

        # Dosyaya yazma işlemi
        with open('output.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(f"{'YIL':<8} {'AY':<5} {'DEGER':<10}\n")
            output_file.write("-" * 25 + "\n")
            output_file.writelines(parsed_data)
