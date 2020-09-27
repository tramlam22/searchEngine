import scrapy
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from items import Product



class EtsyHaikyuuSpider(scrapy.Spider):
    name = 'etsy_haikyuu'
    allowed_domains = ['www.etsy.com']
    start_urls = [
        'https://www.etsy.com/search?q=haikyuu/',
    ]



    #custom_settings={ 'FEED_URI': "etsy_haikyuu.csv" }

    count = 0
        

    def parse(self, response):
        print("processing:" + response.url)

        #extract data w/ css selector
        product_name = response.css('.text-gray.text-truncate.mb-xs-0.text-body::text').extract()
        price = response.css('.currency-value::text').extract()

        #extract data w/ xpath
        shop_name = response.xpath("""//div[@class='v2-listing-card__shop']
                                    /p[@class='text-gray-lighter text-body-smaller display-inline-block']
                                    /text()
                                """).extract()
        product_url = response.xpath("""//div[@class='js-merch-stash-check-listing  v2-listing-card position-relative flex-xs-none ']
                                    /a/@href
                                """).extract()
        image_url = response.xpath("""//img[@class='width-full wt-height-full display-block position-absolute ']
                                    /@src
                                """).extract()

        row_data = zip(product_name, price, shop_name, product_url, image_url)

        #making extracted data row wise
        for item in row_data:
            #create dictionary to store info
            # info = {
            #     'product_url': item[3],
            #     'image_url': item[4],
            #     'product_name': item[0].lower(),
            #     'price': item[1],
            #     'shop_name': item[2].lower(),
            # }
          
            info = Product()
            info['product_url'] = item[3]
            info['image_url'] = item[4]
            info['product_name'] = item[0].lower().strip().replace("\n","")
            info['price'] = item[1]
            info['shop_name'] = item[2].lower()

            #yield or give info to scrapy
            yield info


        #  crawls to the next page
        NEXT_PAGE_SELECTOR = '.wt-action-group__item-container a::attr(href)'
        #next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        next_page = response.css(NEXT_PAGE_SELECTOR)[-1].extract()
        if next_page and self.count != 15:
            self.count += 1
            yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
            )
