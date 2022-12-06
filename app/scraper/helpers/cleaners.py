import re


def modify_xpath_attr_to_text(xpath):
    """
    Used in extract_urls_with_names_selenium,
        to avoid confusion while extracting ProductPages,
        or any other URL/Name data from elements.
    For instance self.categories_discovery_xpath_dict["category_name_xpath"],
        should be @title or text() or any other.
    Xpathses to arguments have to be cleaned to text,
        to be used with Selenium find_elements.
    """
    match = re.search(r"\.?/{1,}@?(\w+)()*", xpath)
    return str(match.group(1))
