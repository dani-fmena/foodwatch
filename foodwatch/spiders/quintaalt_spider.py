import scrapy
from datetime import datetime
from ..helpers import Helpers
from foodwatch.keywords import wordpool


class QuintaaltSpider(scrapy.Spider):
    name = "quinta"
    timeflag = False

    def start_requests(self):
        urls = []

        for keyword in wordpool:
            urls.append("https://5tay42.xetid.cu/module/categorysearch/catesearch?search_query="+keyword)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = 0

        for product in response.css("ul#listado-prod div.product-container"):
            pname = product.css("div.product-image-container a.product_img_link").xpath('@title').get()
            pprice = product.css("div.right-block div.content_price span.price::text").get()

            if pname is None or pprice is None: continue

            phash = Helpers.mkhash(pname, pprice)


            if Helpers.ispresent(phash) is False:

                if self.timeflag is False:
                    yield {
                        '--------- DATE ---------': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "place": self.name.upper()
                    }
                    self.timeflag = True

                count += 1
                yield {'product': pname, 'price': pprice, 'chk': phash}

        if count > 0: Helpers.firetoast(2, count)
