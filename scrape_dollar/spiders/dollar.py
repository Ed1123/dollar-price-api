import scrapy


class DollarSpider(scrapy.Spider):
    name = 'dollar'
    allowed_domains = ['cuantoestaeldolar.pe']
    start_urls = ['http://cuantoestaeldolar.pe/']

    def parse(self, response):
        casas_de_cambio = response.xpath(
            '//div[3]/section/div[1]/div[4]/div[1]/div/div/div[1]'
        )

        for box in casas_de_cambio:
            yield dict(
                name=box.xpath('.//h3/a/text()').get(),
                url=box.xpath('.//h3/a/@href').get(),
                compra=box.xpath('.//div[2]/text()').get(),
                venta=box.xpath('.//div[3]/text()').get(),
            )
