import scrapy


class MerchantpointRuSpider(scrapy.Spider):
    name = "merchantpoint_ru"
    allowed_domains = ["merchantpoint.ru"]
    start_urls = ["https://merchantpoint.ru/brand/4390"]  # для мотобайков

    def parse(self, response: scrapy.http.Response):
        org_description = response.xpath("//div[contains(@class, 'description_brand')]/text()").get()
        merchant_urls = response.xpath("//table[@class='finance-table']//a/@href").getall()

        yield from response.follow_all(
            urls=merchant_urls,
            cb_kwargs={"org_description": org_description},
            callback=self.parse_merchant,
        )

    def parse_merchant(self, response: scrapy.http.Response, org_description: str):
        return {
            "merchant_name": response.xpath("//h1/text()").get(),
            "mcc": response.xpath("//p/a[contains(@href,'mcc')]/@href").get(),
            "address": response.xpath("//div//p[contains(.,'Адрес')]/text()").get(),
            "geo_coordinates": response.xpath("//div//p[contains(.,'Геокоординаты')]/text()").get(),
            "org_name": response.xpath("//p/a[contains(@href,'brand')]/text()").get(),
            "org_description": org_description,
            "source_url": response.url,
        }
