import scrapy


class ChitaiGorodRuSpider(scrapy.spiders.SitemapSpider):
    name = "chitai_gorod_ru"
    allowed_domains = ["chitai-gorod.ru"]
    start_urls = ["https://chitai-gorod.ru"]

    sitemap_urls = ("https://chitai-gorod.ru/sitemap/books-series1.xml", )
    sitemap_follow = []
    sitemap_rules = [("/product", "parse")]

    custom_settings = {
        'ITEM_PIPELINES': {
            "cu_crawling_2.pipelines.CuCrawling2PipelineMongoDB": 300,
        },
        # to stop as fast as limit will be exceeded
        "CLOSESPIDER_ITEMCOUNT": 30,
    }

    def parse(self, response: scrapy.http.Response):
        book_urls = ""

        yield from response.follow_all(
            urls=book_urls,
            cb_kwargs={"org_description": org_description},
            callback=self.parse_book,
        )

    def parse_book(self, response: scrapy.http.Response):
        return {
            "title": "",
            "author": "",
            "description": "",
            "price_amount": "",
            "price_currency": "",
            "rating_value": "",
            "rating_count": "",
            "publication_year": "",
            "isbn": "",
            "pages_cnt": "",
            "publisher": "",
            "book_cover": "",
            "source_url": response.url,
        }
