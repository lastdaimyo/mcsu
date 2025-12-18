import scrapy

CURRENCY_MAPING = {
    "₽": "RUB",
}
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

    @staticmethod
    def _extract_price_info(response: scrapy.http.Response) -> tuple[float, str]:
        old_price_raw = response.xpath("//span[contains(@class,'product-offer-price__old-text')]/text()").get()
        if old_price_raw:
            old_price_parts = old_price_raw.replace("&nbsp;", "").strip().split(" ")
            return int(old_price_parts[0]), CURRENCY_MAPING[old_price_parts[1]]

        new_price = response.xpath("//div[@class='product-offer']//meta[@itemprop='price']/@content").get()
        if not new_price:
            return 0, "₽"

        if '.' in new_price:
            new_price = new_price.split('.')[0]
        new_currency = response.xpath("//div[@class='product-offer']//meta[@itemprop='priceCurrency']/@content").get()
        return int(new_price), new_currency

    def parse(self, response: scrapy.http.Response):
        price_amount, price_currency = self._extract_price_info(response)

        return {
            "title": response.xpath("//h1/text()").extract_first(),
            "author": response.xpath("//ul[@class='product-authors']//li/a/text()").get(default="-"),
            "isbn": response.xpath("//div[@id='properties']//span[@itemprop='isbn']/span/text()").get(default="-"),
            "description": response.xpath("//div[contains(@class, 'product-description')]/text()").get(),
            "price_amount": price_amount,
            "price_currency": price_currency,
            "rating_value": response.xpath("//span[@class='product-rating-detail__count']/text()").get(),
            "rating_count": response.xpath("//span[@class='product-rating__votes']/span[contains(., 'оценки')]/@content").get(),
            "publication_year": response.xpath("//span[@itemprop='datePublished']/span/text()").get(),
            "pages_cnt": response.xpath("//div[@id='properties']//span[@itemprop='numberOfPages']/span/text()").get(),
            "publisher": response.xpath("//span[@itemprop='publisher']/@content").get(),
            "book_cover": response.xpath("//div[@class='product-preview']//img/@src").get(),
            "source_url": response.url,
        }
