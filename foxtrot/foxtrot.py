from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

AVAILABLE = ["В наявності", "Закінчується"]
FOXTROT_BASE = "https://www.foxtrot.com.ua"


def get_urls(link):
    request = requests.get(link).text
    soup = BeautifulSoup(request, 'html.parser')
    hrefs = soup.find_all("div", "card__image")

    urls = []
    for div_element in hrefs:
        a_el = div_element.find_all("a", href=True)
        urls.append(FOXTROT_BASE + a_el[0]['href'])
    return urls


def is_available(url):
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    div_el = soup.find(class_="product-box__status")

    if div_el is None:
        return False

    span_el = div_el.find("span").text
    return span_el in AVAILABLE


def filter_by_available(urls):
    return [url for url in urls if is_available(url)]


def get_main_blocks(soup):
    return soup.find_all("div", class_="main-details__block")


def get_name_and_value(block):
    return get_name(block), get_value(block)


def get_name(block):
    return block.find("span").text.strip(" \n")


def get_value(block):
    span_el = block.find(class_="main-details__item_value").find("span")
    p_el = span_el.find("p")
    if p_el is not None:
        text = p_el.text
    else:
        text = span_el.find("a").text

    return text.strip(" \n")


def get_properties(url):
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')

    main_blocks = get_main_blocks(soup)
    props = {'link': str(url)}
    for block in main_blocks:
        name, value = get_name_and_value(block)
        props[name] = value
    return props


def props_to_df(props):
    return pd.DataFrame([props])


def concat_df(*args):
    return pd.concat(*args, axis=0)


def create_df(urls):
    dfs = [props_to_df(get_properties(i)) for i in urls]
    return concat_df(tuple(dfs))


def check_listing_pagination(url):
    paginated_class = "listing__pagination"
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    pagination = soup.find(class_=paginated_class)
    return pagination is not None


def get_number_of_pages(url):
    if not check_listing_pagination(url):
        return url

    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    paginated_class = "listing__pagination"
    pagination = soup.find(class_=paginated_class)
    last_page = pagination.find_all("a")[-2].text
    return int(last_page)


def get_pages(url):
    if not check_listing_pagination(url):
        return [url]

    last_page = get_number_of_pages(url)
    if "page=1" in url:
        return [url.replace("page=1", f"page={i}") for i in range(1, last_page+1)]
    return [url] + [url + f"&page={i}" for i in range(2, last_page+1)]


def get_urls_from_pages(pages):
    urls = []
    for page in pages:
        urls += get_urls(page)
    return urls


def main():
    url = "https://www.foxtrot.com.ua/uk/search?query=%D0%BF%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%96+%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%B8&page=1"
    urls = get_urls_from_pages(get_pages(url))
    final_df = create_df(urls)
    final_df.to_excel("output2.xlsx", sheet_name="Пральні машини", index=True)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Foxtrot parsed in: {(end-start):.3f}s")
