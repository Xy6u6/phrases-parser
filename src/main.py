import json
import logging as log
import os
from pprint import pprint

import scrapper as sc
from src.gcp import upload_to_cloud


def main():
    log.basicConfig(format='%(levelname)s:%(message)s', level='INFO')
    log.info('run')
    urls = sc.get_top_ten_tags()
    log.info('got list of URLS')
    dict_of_quotes = {}
    # scrapping urls
    for item in urls[0:2]:
        log.info(f'scrapping URLS: {urls.index(item) + 1}th of {len(urls)} pages, {item}')
        tag = item[32:len(item) - 6]
        dict_of_quotes[tag] = sc.parse_phrases(item)
    with open('tmp/tmp.json', 'w', encoding='utf-8') as f:
        pprint(dict_of_quotes)
        json.dump(dict_of_quotes, f, indent=4)

    # write to files
    sc.write_phrases_to_json(dict_of_quotes)
    # sc.write_phrases_to_txt(dict_of_quotes)
    # # upload to gcp
    # list_of_files = os.listdir("/tmp/parser/")
    # for file in list_of_files:
    #     log.info(f'uploading {file}')
    #     upload_to_cloud("parser", "/tmp/parser/" + file, file)
    # log.info('all done')


if __name__ == '__main__':
    main()
