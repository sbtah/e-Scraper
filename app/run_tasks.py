from tasker.logic import ScrapingTasker

with ScrapingTasker() as scraper:
    scraper.discover_all_child_categories()
