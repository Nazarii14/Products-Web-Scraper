from bs4 import BeautifulSoup

import requests
import time


def get_urls_from_page(link):
    class_ = "image-carousel"
    request = requests.get(link).text
    soup = BeautifulSoup(request, 'html.parser')
    hrefs = soup.find_all("a", class_=class_)

    urls = []
    for a_el in hrefs:
        url = a_el['href']
        urls.append(url)
    return urls


# def is_available(url):
#     pass
#
#
# def filter_by_available(urls):
#     pass


def get_pages(url):
    if not check_pagination(url):
        return [url]

    number_of_pages = get_number_of_pages(url)
    if 1:
        pass


def create_df(urls):
    pass
    # dfs = [props_to_df(get_properties(i)) for i in urls]
    # return concat_df(tuple(dfs))


def get_number_of_pages(url):
    class_ = "pagination__item"
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    pagination = soup.find_all(class_=class_)
    return int(pagination[-1].text) or None


def check_pagination(url):
    class_ = "pagination"
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    pagination = soup.find(class_=class_)
    return pagination is not None


def main():
    url = "https://allo.ua/ua/catalogsearch/result/?q=%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D1%81%D0%B0%D0%BC%D0%BE%D0%BA%D0%B0%D1%82%D0%B8&cat=3522"
    # urls = get_urls_from_pages(get_pages(url))
    # final_df = create_df(urls)
    # final_df.to_excel("output2.xlsx", sheet_name="Пральні машини", index=True)
    print(get_urls_from_page(url))


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Execution time: {end-start} seconds")
