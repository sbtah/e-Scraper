# Early prototype of Ecommerce Scraper v0.02

e-Scraper technologies used :
- Django,
- Selenium,
- lxml,
- Postgresql,
- Redis, 
- Celery,
- Celery Beat,
- pandas,
- RabbitMq,
- Docker,
- Chrome Grid.

Current Functionalities:
- Validate status code for requested WebPage and proceed if code is OK.
- Find Product URLS/Names on requested Category Page.
- Extract Meta data froch each requested Page.
- Parse CategoryPages with pagination and extract ProductPage data from each page.

- Scrape products from specified store,
- Track specified products or individual pages,
- Generate XLSX rapports,
- Send emails about changes on site,
- Do basic SEO checks on tracked site,


Project is in WIP state.
