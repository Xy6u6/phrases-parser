import requests
from bs4 import BeautifulSoup


def get_top_ten_tags() -> list:
    """func returns urls with top ten tags to parse"""
    url = 'https://quotes.toscrape.com'
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    top_ten_tags = sp.find('h2', string="Top Ten tags").findParent()
    hrefs = top_ten_tags.findAll('a', class_='tag')
    urls_list = [url + str(i.get('href')) + 'page/' for i in hrefs]
    return urls_list


def parse_phrases(url: str) -> list:
    """func to parse phrases and authors from url into list"""
    list_of_quotes = []
    page = 1
    while True:
        res = requests.get(url + str(page))
        sp = BeautifulSoup(res.text, 'lxml')
        if 'No quotes found!' in str(sp.contents):
            return list_of_quotes
        else:
            phrases = sp.findAll('span', class_='text')
            authors = sp.findAll('small', class_='author')
            for counter, phrase in enumerate(phrases):
                list_of_quotes.append(f'{counter + 1}. {phrase.text} by: {authors[counter].text}')
            page += 1


def check_next_page(url):
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    try:
        sp.find('li', class_='next').find('a').get('href')
        return True
    except AttributeError:
        return False


def write_phrases_to_txt(phrases: dict):
    pass


if __name__ == '__main__':
    urls = get_top_ten_tags()
    dict_of_qoutes = {}
    for item in urls:
        tag = item[32:len(item) - 6]
        dict_of_qoutes[tag] = parse_phrases(item)
    print(dict_of_qoutes)
