import requests
from bs4 import BeautifulSoup


def get_top_ten_tags() -> list:
    url = 'https://quotes.toscrape.com'
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    tags = sp.findParent('Top Ten tags').find_all('a', class_='tag')
    urls = [url + str(i.get('href')) + '/page/' for i in tags]
    return urls


# TODO: rename func
def get_quotes(url: str):
    """func to get quotes from url"""
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    tag = sp.find('h3').find('a').text
    quotes = sp.findAll('span', class_='text')
    authors = sp.findAll('small', class_='author')
    for counter, k in enumerate(quotes):
        with open(f'list of {tag} sentences.txt', 'a') as f:
            f.write(f'{counter + 1}. {k.text} by: {authors[counter].text} \n')

    if check_next_page(url):
        nextpage = url + '/page/2'  # TODO: FIX constant 2
        get_quotes(nextpage)
    else:
        return


def check_next_page(url):
    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'lxml')
    try:
        sp.find('li', class_='next').find('a').get('href')
        return True
    except AttributeError:
        return False


if __name__ == '__main__':
    urls = get_top_ten_tags()
    for i in urls:
        print(f'scrapping page {i}')
        get_quotes(i)
