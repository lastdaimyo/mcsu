import scrapy

# For HTML parsing only one web page
# class MerchantpointRuSpider(scrapy.Spider):
#     name = "merchantpoint_ru"
#     allowed_domains = ["merchantpoint.ru"]
#     start_urls = ["https://merchantpoint.ru/brand/4390"]  # для мотобайков
#     USE only custom pipelines
#     custom_settings = {
#         'ITEM_PIPELINES': {
#             "cu_crawling.pipelines.CuCrawlingPipeline": 300,
#         },
#     }

# For XML Parsing
class MerchantpointRuSpider(scrapy.spiders.SitemapSpider):
    name = "merchantpoint_ru"
    allowed_domains = ["merchantpoint.ru"]
    sitemap_urls = ("https://merchantpoint.ru/sitemap/brands.xml", )
    sitemap_rules = [("/brand", "parse")]

    custom_settings = {
        'ITEM_PIPELINES': {
            "cu_crawling.pipelines.CuCrawlingPipeline": 300,
        },
        # to stop as fast as limit will be exceeded
        "CLOSESPIDER_ITEMCOUNT": 30,
    }

    def parse(self, response: scrapy.http.Response):
        # get валиден только, если от xpath ожидается исключительно один объект
        # getall уже возвращает список объектов
        raw_org_description = response.xpath("//div[contains(@class, 'description_brand')]//text()").getall()
        # склеивание на уровне паука дешевле, чем обрабатывать в pipeline
        # в pipeline лучше обеспечивать обработку "тяжелых" объектов с привлечением внешних зависимостей
        org_description = " ".join(raw_org_description)
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
