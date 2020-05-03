import scrapy
from datetime import datetime
from ..helpers import Helpers
from foodwatch.keywords import wordpool


class Carlos3Spider(scrapy.Spider):
    name = "carlos3"
    timeflag = False

    def start_requests(self):
        urls = []

        for keyword in wordpool:
            urls.append("https://www.tuenvio.cu/carlos3/Search.aspx?keywords=%22"+keyword+"%22")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = 0

        for product in response.css("div.thumbSetting"):
            pname = product.css("div.thumbTitle>a::text").get()
            pprice = product.xpath("div[2]/span/text()").get()
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

        if count > 0: Helpers.firetoast(1, count)
