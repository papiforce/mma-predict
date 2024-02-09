# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class MmaItem(Item):
    Name = scrapy.Field()
    Weight = scrapy.Field()
    Win = scrapy.Field()
    Lose = scrapy.Field()
    Draw = scrapy.Field()
    DOB = scrapy.Field()
    Height = scrapy.Field()
    Reach = scrapy.Field()
    Stance = scrapy.Field()
    Significant_Strikes_Landed_per_Minute = scrapy.Field()
    Significant_Striking_Accuracy = scrapy.Field()
    Significant_Strikes_Absorbed_per_Minute = scrapy.Field()
    Significant_Strike_Defence = scrapy.Field()
    Average_Takedowns_Landed_per_15_minutes = scrapy.Field()
    Takedown_Accuracy = scrapy.Field()
    Takedown_Defense = scrapy.Field()
    Average_Submissions_Attempted_per_15_minutes = scrapy.Field()
    WL = scrapy.Field()
    Fighters = scrapy.Field()
    Events = scrapy.Field()
    Record = Field()
    Fighters_and_Events = Field()
