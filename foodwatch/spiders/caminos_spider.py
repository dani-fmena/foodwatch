import scrapy
from datetime import datetime
from win10toast import ToastNotifier
from foodwatch.keywords import wordpool


class CaminosSpider(scrapy.Spider):
    name = "caminos"
    timeflag = False
    toaster = ToastNotifier()

    def start_requests(self):
        urls = []

        for keyword in wordpool:
            urls.append("https://www.tuenvio.cu/4caminos/Search.aspx?keywords=%22" + keyword + "%22")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.timeflag is False:
            yield {'--- DATE ---': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "place": self.name}
            self.timeflag = True

        for product in response.css("div.thumbSetting"):
            yield {
                'product': product.css("div.thumbTitle>a::text").get(),
                'price': product.xpath("div[2]/span/text()").get(),
            }

        pcount = len(response.css("div.thumbSetting"))
        if pcount > 0:
            self.toaster.show_toast(
                "Productos encontrados en Cuatro Caminos",
                "Encontrados %s productos" % str(pcount),
                duration=50
            )
