import scrapy
from datetime import datetime
from win10toast import ToastNotifier
from foodwatch.keywords import wordpool


class QuintaSpider(scrapy.Spider):
    name = "quinta"
    timeflag = False
    toaster = ToastNotifier()

    def start_requests(self):
        urls = []

        for keyword in wordpool:
            urls.append("https://5tay42.xetid.cu/module/categorysearch/catesearch?search_query="+keyword)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.timeflag is False:
            yield {'--- DATE ---': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "place": self.name}
            self.timeflag = True

        for product in response.css("ul#listado-prod div.product-container div.right-block"):
            yield {
                'text': product.css("p.product-desc::text").get(),
                'price': product.css("div.content_price span.price::text").get(),
            }

        pcount = len(response.css("ul#listado-prod div.product-container div.right-block"))
        if pcount > 0:
            self.toaster.show_toast(
                "Productos encontrados en 5tay42",
                "Encontrados %s productos" % str(pcount),
                duration=50
            )
