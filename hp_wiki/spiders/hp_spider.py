import re
from io import StringIO
from html.parser import HTMLParser

import scrapy

from hp_wiki.items import HpWikiItem



# Some HTML tags need to be removed
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()


class HPSpider(scrapy.Spider):
    name = 'hp_spider'

    domain = 'harrypotter.fandom.com'
    allowed_domains = [domain]
    harry = 'wiki/Harry_Potter'
    hermione = 'wiki/Hermione_Granger'
    ron = 'wiki/Ronald_Weasley'
    start_urls = [
      f'https://{domain}/{harry}',
      f'https://{domain}/{hermione}',
      f'https://{domain}/{ron}',
      ]


    def parse(self, response):
      page_path = response.url[len("https://"+self.domain):]

      title = response.css('h1.page-header__title::text').get()

      # These contain the good text
      p_tags = '.mw-parser-output > p::text'
      a_tags = '.mw-parser-output > p > a::text'
      b_tags = '.mw-parser-output > p > b::text'
      i_tags = '.mw-parser-output > p > i::text'
      li_tags =  '.mw-parser-output > p > ul > li *::text'

      # Section titles used for organizing text into chunks
      section_titles = ".mw-parser-output .mw-headline"

      # Combine all css selectors into one
      combined = ",".join([p_tags, a_tags, b_tags, i_tags, li_tags, section_titles])

      # Get texts using the combined css selector
      texts = response.css(combined).getall()

      # Get the section names
      sections = response.css(section_titles).getall()

      # stop_index indicates when the junk sections have been reached
      sections_to_avoid = ["Media", "Etymology", "Behind the scenes", "Gallery","External Links","Appearances", "Notes and references"]
      stop_index = len(texts)
      for i, t in enumerate(texts):

        # If there is a section span
        if any([re.search(r"<span.*{}".format(x), t) for x in sections_to_avoid]):
          stop_index = i
          break

      # First section is the summary at the top of page that doesn't have a section header in HTML
      current_section = "Summary"
      current_texts = []
      for t in texts[:stop_index]:

        # Check for section span tag
        if re.search(r"<span.*>", t):
          
          # If a section span tag has been found, then "current_section" is over.
          # If there are texts saved, save as an Item.
          if len(current_texts) > 0:
            yield HpWikiItem({
              "title": f"{title} - {current_section}",
              "text": "".join(current_texts),
              "path": page_path
            })

            # Reset for next section
            current_texts = []
            current_section = strip_tags(t)

          else:
            # If "current_texts" is empty, there could be multiple sections back-to-back.
            # Here is an example: https://harrypotter.fandom.com/wiki/Harry_Potter#Biography
            current_section += " " + strip_tags(t)
        else:

          # If it isn't a section, it is good text to append to the list.
          current_texts.append(t)

      # Unless the last item in "texts" is a section, "current_texts" will not be empty.
      if current_texts:
        yield HpWikiItem({
          "title": f"{title} - {strip_tags(current_section)}",
          "text": "".join(current_texts),
          "path": page_path
        })

      # Follow any link in a paragraph
      next_page = response.css('.mw-parser-output > p > a::attr(href)').getall()
      if next_page:
        for page in next_page:
          yield scrapy.Request("https://"+self.domain+page, callback=self.parse)ƒ