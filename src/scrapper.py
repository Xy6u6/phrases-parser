import os
import requests
from bs4 import BeautifulSoup
import logging as log
import json


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
                list_of_quotes.append(
                    {"qoute": str(phrase.text).replace("“", "").replace("”", ""), "author": authors[counter].text})
            page += 1


def write_phrases_to_txt(dict_of_quotes: dict):
    """function collect phrases to files named like dict keys"""
    os.makedirs('/tmp/parser/', exist_ok=True)
    for key in dict_of_quotes.keys():
        log.info(f'writing {key} qoutes')
        with open(f'/tmp/parser/{key}_quotes_of_great_men.txt', 'a') as f:
            for value in dict_of_quotes[key]:
                f.write(f'{value} \n')


def write_phrases_to_json(dict_of_quotes: dict):
    """function collect phrases to files named like dict keys"""
    os.makedirs('/tmp/parser/', exist_ok=True)
    for key in dict_of_quotes.keys():
        log.info(f'writing {key} qoutes')
        with open(f'/tmp/parser/{key}_quotes_of_great_men.json', 'w') as f:
            json.dump(dict_of_quotes[key], f, indent=4)


if __name__ == '__main__':
    with open('tmp/tmp.json','r') as f:
        dict_of_quotes = json.load(f)
        write_phrases_to_json(dict_of_quotes)
