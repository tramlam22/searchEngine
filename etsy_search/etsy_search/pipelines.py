# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from searchApp.models import productItem

class EtsySearchPipeline(object):
    def process_item(self, item, spider):
        # product = productItem()

   
        # product.product_name = item['product_name']
        # product.product_url = item['product_url']
        # product.price = item['price']
        # product.shop_name = item['shop_name']
        # product.image_url = item['image_url']
        
        item.save()
        return item
