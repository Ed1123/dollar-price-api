import scrapy


class DollarSpider(scrapy.Spider):
    name = 'dollar'
    allowed_domains = ['cuantoestaeldolar.pe']
    start_urls = ['http://cuantoestaeldolar.pe/']

    def parse(self, response):
        casas_de_cambio = response.xpath(
            '/html/body/div[3]/section/div[1]/div[3]/div[1]/div/div'
        )

        for box in casas_de_cambio:
            if 'header' in box.xpath('./@class').get():
                continue
            yield dict(
                name=box.xpath('.//h3/a/text()').get(),
                url=box.xpath('.//h3/a/@href').get(),
                compra=box.xpath('./div[1]/div[2]/text()').get().strip(),
                venta=box.xpath('./div[1]/div[3]/text()').get().strip(),
            )
