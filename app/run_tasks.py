"""
Test scraping tasks. Works with database.
"""

from tasker.logic import ScrapingTasker

with ScrapingTasker() as scraper:
    scraper.discover_main_categories()
    scraper.refresh_current_session()
    scraper.discover_all_child_categories()
    scraper.refresh_current_session()
    scraper.discover_all_sub_categories()
    scraper.refresh_current_session()
    scraper.discover_all_products()
