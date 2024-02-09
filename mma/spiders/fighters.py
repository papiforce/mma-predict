import scrapy
import json
from datetime import datetime

class FighterSpider(scrapy.Spider):
    name = "fighter"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/fighters"]

    def parse(self, response):
        # Extract and print each fighter's first name
        fighter_links = response.css('td.b-statistics__table-col a::attr(href)').getall()
        for link in fighter_links:
            if link is not None:
                yield response.follow(link, self.parse_fighter)

        # Follow pagination links
        next_pages = response.css('ul.b-statistics__paginate a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def parse_fighter(self, response):
        # Extract data from the fighter's page
        full_name = response.css('span.b-content__title-highlight::text').get().strip()
        weight = response.css('li.b-list__box-list-item:contains("Weight:")::text').getall()[-1].strip()
        record = response.css('span.b-content__title-record::text').get().strip().split(':')[1]
        win, lose, draw = record.split('-')
        dob = response.css('li.b-list__box-list-item:contains("DOB:")::text').getall()[-1].strip()

        # Extract additional personal information
        height = response.css('li.b-list__box-list-item:contains("Height:")::text').getall()[-1].strip()
        reach = response.css('li.b-list__box-list-item:contains("Reach:")::text').getall()[-1].strip()
        stance = response.css('li.b-list__box-list-item:contains("STANCE:")::text').getall()[-1].strip()

        # Extract additional statistics
        slpm = response.css('li.b-list__box-list-item:contains("SLpM:")::text').getall()[-1].strip()
        str_acc = response.css('li.b-list__box-list-item:contains("Str. Acc.:")::text').getall()[-1].strip()
        sapm = response.css('li.b-list__box-list-item:contains("SApM:")::text').getall()[-1].strip()
        str_def = response.css('li.b-list__box-list-item:contains("Str. Def:")::text').getall()[-1].strip()
        td_avg = response.css('li.b-list__box-list-item:contains("TD Avg.:")::text').getall()[-1].strip()
        td_acc = response.css('li.b-list__box-list-item:contains("TD Acc.:")::text').getall()[-1].strip()
        td_def = response.css('li.b-list__box-list-item:contains("TD Def.:")::text').getall()[-1].strip()
        sub_avg = response.css('li.b-list__box-list-item:contains("Sub. Avg.:")::text').getall()[-1].strip()

        # Extract W/L data from the table of matches
        wl_data = response.css('tr.b-fight-details__table-row td.b-fight-details__table-col p.b-fight-details__table-text a.b-flag i.b-flag__inner i.b-flag__text::text').getall()

        # Store the data in a dictionary
        fighter_data = {
            'Name': full_name,
            'Weight': weight,
            'Win': win,
            'Lose': lose,
            'Draw': draw,
            'DOB': dob,
            'Height': height,
            'Reach': reach,
            'Stance': stance,
            'Significant Strikes Landed per Minute': slpm,
            'Significant Striking Accuracy': str_acc,
            'Significant Strikes Absorbed per Minute': sapm,
            'Significant Strike Defence': str_def,
            'Average Takedowns Landed per 15 minutes': td_avg,
            'Takedown Accuracy': td_acc,
            'Takedown Defense': td_def,
            'Average Submissions Attempted per 15 minutes': sub_avg,
            'W/L': wl_data
        }

        # Write the dictionary to a JSON file
        with open('fighters.json', 'a') as f:
            json.dump(fighter_data, f)
            f.write('\n')
