import scrapy
from mma.items import UfcItem

class FightersSpider(scrapy.Spider):
    name = "fighters"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/fighters"]

    def parse(self, response):
        fighter_links = response.css('td.b-statistics__table-col a::attr(href)').getall()
        for link in fighter_links:
            if link is not None:
                yield response.follow(link, self.parse_fighter)

        next_pages = response.css('ul.b-statistics__paginate a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def parse_fighter(self, response):
        item = UfcItem()
        item['Name'] = response.css('span.b-content__title-highlight::text').get().strip()
        item['Weight'] = response.css('li.b-list__box-list-item:contains("Weight:")::text').getall()[-1].strip()
        item['Record'] = response.css('span.b-content__title-record::text').get().strip().split(':')[1].strip()
        item['DOB'] = response.css('li.b-list__box-list-item:contains("DOB:")::text').getall()[-1].strip()
        item['Height'] = response.css('li.b-list__box-list-item:contains("Height:")::text').getall()[-1].strip()
        item['Reach'] = response.css('li.b-list__box-list-item:contains("Reach:")::text').getall()[-1].strip()
        item['Stance'] = response.css('li.b-list__box-list-item:contains("STANCE:")::text').getall()[-1].strip()
        item['Significant_Strikes_Landed_per_Minute'] = response.css('li.b-list__box-list-item:contains("SLpM:")::text').getall()[-1].strip()
        item['Significant_Striking_Accuracy'] = response.css('li.b-list__box-list-item:contains("Str. Acc.:")::text').getall()[-1].strip()
        item['Significant_Strikes_Absorbed_per_Minute'] = response.css('li.b-list__box-list-item:contains("SApM:")::text').getall()[-1].strip()
        item['Significant_Strike_Defence'] = response.css('li.b-list__box-list-item:contains("Str. Def:")::text').getall()[-1].strip()
        item['Average_Takedowns_Landed_per_15_minutes'] = response.css('li.b-list__box-list-item:contains("TD Avg.:")::text').getall()[-1].strip()
        item['Takedown_Accuracy'] = response.css('li.b-list__box-list-item:contains("TD Acc.:")::text').getall()[-1].strip()
        item['Takedown_Defense'] = response.css('li.b-list__box-list-item:contains("TD Def.:")::text').getall()[-1].strip()
        item['Average_Submissions_Attempted_per_15_minutes'] = response.css('li.b-list__box-list-item:contains("Sub. Avg.:")::text').getall()[-1].strip()
        item['WL'] = [result.strip() for result in response.css('tr.b-fight-details__table-row td.b-fight-details__table-col p.b-fight-details__table-text a.b-flag i.b-flag__inner i.b-flag__text::text').getall()]
        item['Fighters_and_Events'] = [event.strip() for event in response.css('tr.b-fight-details__table-row td.b-fight-details__table-col.l-page_align_left p.b-fight-details__table-text a.b-link.b-link_style_black::text').getall()]

        yield item

