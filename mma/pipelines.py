# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class MmaPipeline:
    def open_spider(self, spider):
        self.file = open('fighters.json', 'w')
        self.data = []

    def close_spider(self, spider):
        self.file.write(json.dumps(self.data))
        self.file.close()

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

class DataProcessingPipeline:
    def process_item(self, item, spider):
        win, lose, draw = item['Record'].split('-')
        item['Win'] = win
        item['Lose'] = lose
        item['Draw'] = draw
        del item['Record']

        fighters_and_events = item['Fighters_and_Events']
        fighters = [item.strip() for item in fighters_and_events if not any(event in item for event in ["UFC", "DWCS", "PRIDE","DREAM","Shooto","DEEP","Fury", "dynamite"])]
        events = [item.strip() for item in fighters_and_events if any(event in item for event in ["UFC", "DWCS", "PRIDE","DREAM","Shooto","DEEP","Fury", "dynamite"])]
        item['Fighters'] = fighters
        item['Events'] = events
        del item['Fighters_and_Events']

        return item