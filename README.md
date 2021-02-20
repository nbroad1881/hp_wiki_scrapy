# Scrapy for harrypotter.fandom.com 🧙🏻‍♂️⚡️🤓

A scrapy project that pulls most useful text from pages and follows links.

Able to scrape ~8,000 of the +16,000 pages in an hour.

Gets page titles, section headers, paragraphs, and lists.

Does not get quotes or captions.

## Data
The data that I scraped is in [wiki_data](wiki_data).  
It is stored in a single json file using json lines.
Here is an example of one line.  
```
{"path": "/wiki/Ronald_Weasley", "text": "Ron's wand was damaged in the crash, causing him problems for the entire school year. It backfired when Ron attempted to curse Draco Malfoy in payback for calling Hermione a \"Mudblood\" with the Slug-vomiting Charm, resulting with him burping up slugs and slime. Malfoy's disdain towards Muggle-borns led Ron, Harry, and Hermione to suspect that he was the Heir of Slytherin who opened the Chamber of Secrets that year, unleashing a \"monster\" that began to attack Muggle-born students.\n", "title": "Ronald Weasley - Attempt to curse Malfoy"}
```