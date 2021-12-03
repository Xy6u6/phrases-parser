import os
import requests
from bs4 import BeautifulSoup
import logging as log
from google.cloud import storage


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


def write_phrases_to_txt(dict_of_quotes: dict):
    """function collect phrases to files named like dict keys"""
    os.makedirs('/tmp/parser/', exist_ok=True)
    for key in dict_of_quotes.keys():
        log.info(f'writing {key} qoutes')
        with open(f'/tmp/parser/{key}_quotes_of_great_men.txt', 'a') as f:
            for value in dict_of_quotes[key]:
                f.write(f'{value} \n')


def upload_to_cloud(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    storage_client = storage.Client.from_service_account_json('tmp/gcp_acc.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


if __name__ == '__main__':
    # dict_of_quotes = {'jj': 'n'}
    # write_phrases_to_txt(dict_of_quotes)
    upload_to_cloud("parser", "tmp/somefile.txt", "some_cloud_file.txt")
