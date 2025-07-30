import scrapy
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "narutospider"
    start_urls = [
        "https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu",
    ]

    def parse(self, response):
        for href in (
            response.css("div.smw-columnlist-container")[0]
            .css("a::attr(href)")
            .extract()
        ):
            extracted_data = scrapy.Request(
                "https://naruto.fandom.com" + href, callback=self.parse_jutsu
            )

            return extracted_data

        next_page = response.css("mw-nextlink").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_Jutsu(self, response):
        jutsu_name = response.css("h1.page_header___title::text").extract()[0]
        jutsu_name = jutsu_name.strip()

        div_selector = response.css("div.mw-parser-output")[0]
        div_html = div_selector.extract()

        soup = BeautifulSoup(div_html).find("div")

        yield dict(
            jutsu_name=jutsu_name,
        )
