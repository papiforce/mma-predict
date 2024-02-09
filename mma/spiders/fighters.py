import scrapy


class FightersSpider(scrapy.Spider):
    name = "fighters"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/fighters"]

    def parse(self, response):
        letters = response.css('body > section > div > div > div > div.b-statistics__nav-inner > div > ul > li.b-statistics__nav-item > a::text').extract()

        for letter in letters:
            letter_url = f'http://ufcstats.com/statistics/fighters?char={letter.strip()}&page=all'
            yield scrapy.Request(letter_url, callback=self.parse_letter)

    def parse_letter(self, response):
        fighter_links = response.css('tr.b-statistics__table-row td.b-statistics__table-col a::attr(href)').extract()

        for fighter_link in fighter_links:
            yield scrapy.Request(fighter_link, callback=self.parse_fighter)

        upcoming_fight_links = response.css('tr.b-statistics__table-row td.b-statistics__table-col a::attr(href)').extract()

        for upcoming_fight_link in upcoming_fight_links:
            absolute_upcoming_fight_link = f"{response.url}{upcoming_fight_link}"
            # yield scrapy.Request(absolute_upcoming_fight_link, callback=self.parse_upcoming_fight)

    def parse_fighter(self, response):
        fighter_name = response.css('span.b-content__title-highlight::text').get().strip()

        fighter_stats = {
            'fighter_name': fighter_name,
            'height': response.css('body > section > div > div > div.b-list__info-box.b-list__info-box_style_small-width.js-guide > ul > li:nth-child(1)::text').extract()[1].strip(),
            'weight': response.css('body > section > div > div > div.b-list__info-box.b-list__info-box_style_small-width.js-guide > ul > li:nth-child(2)::text').extract()[1].strip(),
        }

        print(fighter_stats)

        previous_fight_links = response.css('tr.b-fight-details__table-row td.b-fight-details__table-col:nth-child(2) a::attr(href)').extract()

        previous_fights = []

        for previous_fight_link in previous_fight_links:
            absolute_previous_fight_link = response.urljoin(previous_fight_link)
            # yield scrapy.Request(absolute_previous_fight_link, callback=self.parse_previous_fight, meta={'previous_fights': previous_fights})

        upcoming_fight_links = response.css('tr.b-fight-details__table-row td.b-fight-details__table-col:nth-child(3) a::attr(href)').extract()

        upcoming_fights = []

        for upcoming_fight_link in upcoming_fight_links:
            absolute_upcoming_fight_link = response.urljoin(upcoming_fight_link)
            # yield scrapy.Request(absolute_upcoming_fight_link, callback=self.parse_upcoming_fight, meta={'upcoming_fights': upcoming_fights})

        # fighter_stats['previous_fights'] = response.meta['previous_fights']
        # fighter_stats['upcoming_fights'] = response.meta['upcoming_fights']
        # yield fighter_stats

    def parse_previous_fight(self, response):
        previous_fight_stats = {
            'date': response.css('span.b-fight-details__text-date::text').get().strip(),
            'result': response.css('div.b-fight-details__persons-side.i-b-fight-details__persons-side div:nth-child(1) i::text').get().strip(),
        }

        response.meta['previous_fights'].append(previous_fight_stats)
        yield previous_fight_stats

    def parse_upcoming_fight(self, response):
        upcoming_fight_stats = {
            'date': response.css('span.b-fight-details__text-date::text').get().strip(),
        }

        response.meta['upcoming_fights'].append(upcoming_fight_stats)
        yield upcoming_fight_stats