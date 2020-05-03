from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from foodwatch.spiders.caminos_spider import CaminosSpider
from foodwatch.spiders.carlos3_spider import Carlos3Spider
from foodwatch.spiders.quita_spider import QuintaSpider


settings = get_project_settings()
process = CrawlerProcess(settings)
# process = CrawlerProcess()

process.crawl(Carlos3Spider)
process.crawl(CaminosSpider)
process.crawl(QuintaSpider)

process.start()     # the script will block here until all crawling jobs are finished
