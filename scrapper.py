import requests
from bs4 import BeautifulSoup


def get_top_ten_tags() -> list:
    url = 'https://quotes.toscrape.com'
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    top_ten_tags = sp.find('h2', string="Top Ten tags").findParent()
    hrefs = top_ten_tags.findAll('a', class_='tag')
    urls_list = [url + str(i.get('href')) + 'page/' for i in hrefs]
    return urls_list


# TODO: rename func
def parse_phrases(url: str) -> list:
    """func to parse phrases and authors from url into list"""
    list_of_quotes = []

    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    tag = sp.find('h3').find('a').text
    phrases = sp.findAll('span', class_='text')
    authors = sp.findAll('small', class_='author')
    for counter, phrase in enumerate(phrases):
        list_of_quotes.append(f'{counter + 1}. {phrase.text} by: {authors[counter].text} \n')

    return list_of_quotes


def check_next_page(url):
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    try:
        sp.find('li', class_='next').find('a').get('href')
        return True
    except AttributeError:
        return False


def write_phrases_to_txt(phrases: list):
    pass


if __name__ == '__main__':
    urls = get_top_ten_tags()
    print(parse_phrases(urls[0]))
