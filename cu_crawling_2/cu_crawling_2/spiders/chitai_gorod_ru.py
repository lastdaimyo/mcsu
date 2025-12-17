import scrapy


class ChitaiGorodRuSpider(scrapy.spiders.SitemapSpider):
    name = "chitai_gorod_ru"
    allowed_domains = ["chitai-gorod.ru"]

    sitemap_urls = ("https://chitai-gorod.ru/sitemap.xml", )
    sitemap_follow = ["/products"]
    sitemap_rules = [("product/", "parse")]

    custom_settings = {
        'ITEM_PIPELINES': {
            "cu_crawling_2.pipelines.CuCrawling2PipelineMongoDB": 300,
        },
        # to stop as fast as limit will be exceeded
        "CLOSESPIDER_ITEMCOUNT": 30,
    }

    def parse(self, response: scrapy.http.Response):
        return {
            "title": response.xpath("//h1/text()").extract_first(),
            "isbn": response.xpath("//span[@itemprop='isbn']/span/text()").get(),
        }
