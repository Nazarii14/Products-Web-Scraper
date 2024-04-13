from bs4 import BeautifulSoup
import requests
import pandas as pd

AVAILABLE = ["В наявності", "Закінчується"]
FOXTROT_BASE = "https://www.foxtrot.com.ua"


def get_urls(link):
    request = requests.get(link).text
    soup = BeautifulSoup(request, 'html.parser')
    hrefs = soup.find_all("div", "card__image")

    urls = []
    for i, div_element in enumerate(hrefs):
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
    class_ = "main-details__block"
    main_blocks = soup.find_all("div", class_=class_)
    return main_blocks


def get_name_and_value(block):
    return get_name(block), get_value(block)


def get_name(block):
    div_el = block.find("span")
    name = div_el.text.strip(" \n")
    return name


def get_value(block):
    span_el = block.find(class_="main-details__item_value").find("span")
    p_el = span_el.find("p")
    text = ''
    if p_el is not None:
        text = p_el.text
    else:
        a_el = span_el.find("a")
        text = a_el.text

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


def main():
    link = "https://www.foxtrot.com.ua/uk/shop/girobordi_elektrosamokat.html"
    urls = get_urls(link)
    dfs = []
    for i in urls:
        dfs.append(props_to_df(get_properties(i)))
    final_df = concat_df(tuple(dfs))
    final_df.to_excel("output1.xlsx", sheet_name="Електросамокати", index=True)


if __name__ == "__main__":
    main()
