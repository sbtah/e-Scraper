from scraper.logic.medium import EcommerceScraper
from scraper.helpers.helpers import extract_text_child_category_name

with EcommerceScraper(use_selenium=True, use_python=False) as scraper:
    # scraper.request_url(
    #     "https://www.castorama.pl/sruby-do-deski-tycner-b-203-komplet-id-37638.html"
    # )
    # element = scraper.pick_store_by_name_top("Koszalin")
    # print(scraper.parse_product_page(element_to_parse=element))

    ### TODO:
    ### Find all products on given page with parsing through all pages.
    # element = scraper.request_url(
    #     "https://www.castorama.pl/produkty/budowa/drewno-budowlane-i-plyty-drewnopochodne/drewno-konstrukcyjne.html"
    # )
    # genex = scraper.extract_products_from_all_pages(html_element=element)
    # for x in genex:
    #     print(x)

    # # # TODO:
    # # Find all ChildCategories on HtmlElement and related products.
    scraper.request_url(
        "https://www.castorama.pl/produkty/budowa/drewno-budowlane-i-plyty-drewnopochodne.html"
    )
    element = scraper.pick_store_by_name_top("Koszalin")
    child_categories = scraper.extract_urls_with_names(
        html_element=element,
        xpath_to_search='.//h2[contains(@class, "heading-base")]//a[contains(@class, "menu-with")]',
        name_xpath="./text()",
    )
    # for x in child_categories:
    #     print(x)

    # Names here needed some special parsing since they were coming with \n and \t symbols.
    for x, y in child_categories:
        print(f"DEBUG:{extract_text_child_category_name(y)}")
        new_el = scraper.request_url(x)
        # Find all products for all pages.
        genex = scraper.extract_products_from_all_pages(html_element=new_el)
        for x in genex:
            print(x)
    # product_elem = scraper.request_url(x[0])
    # scraper.parse_product_page(element_to_parse=product_elem)

    # # TODO:
    # # Find all SubCategories on HtmlElement.
    # element = scraper.request_url("https://www.castorama.pl/produkty/budowa.html")
    # sub_categories = scraper.extract_urls_with_names(
    #     html_element=element,
    #     xpath_to_search='.//h4[contains(@class, "category")]//a[1]',
    #     name_xpath="./@title",
    # )
    # for x in sub_categories:
    #     print(x)

    # # ## TODO:
    # ### Parse all stores. Task. No Selenium. Scout task.
    # element = scraper.request_url(scraper.stores_url)
    # genex = scraper.extract_urls_with_names(
    #     html_element=element,
    #     xpath_to_search=scraper.local_stores_elements_xpath,
    #     name_xpath=".//text()",
    # )
    # for x in genex:
    #     print(x)

    # # ## TODO:
    # # ### Parse all main categories. Task. No Selenium. Scout task.
    # element = scraper.python_get(scraper.main_url)
    # elements = scraper.extract_urls_with_names(
    #     html_element=element,
    #     xpath_to_search=scraper.main_categories_elements_xpath,
    #     name_xpath="./@title",
    # )
    # for x in elements:
    #     print(x)

    # # # ## TODO:
    # # # ### Parse all main categories. Task. Selenium.
    # element = scraper.request_url(scraper.main_url)
    # categories = scraper.extract_urls_with_names(
    #     html_element=element,
    #     xpath_to_search=scraper.main_categories_elements_xpath,
    #     name_xpath="./@title",
    # )
    # for x in categories:
    #     print(x)

    ### TODO:
    ### Validation of request. Check if user agent and ip is correct.
    # scraper.request_url("http://www.ipconfig.org/")
    # time.sleep(5)

    # ## TODO:
    # ## Close cookies policy upon request.
    # element = scraper.request_url(scraper.main_url)
    # scraper.close_cookies_policy(
    #     html_element=element,
    #     xpath_to_search=scraper.cookies_policy_close_button,
    # )
