import logging as log
import src.scrapper as sc


def main():
    log.basicConfig(format='%(levelname)s:%(message)s', level='INFO')
    log.info('run')
    urls = sc.get_top_ten_tags()
    log.info('got list of URLS')
    dict_of_quotes = {}
    for item in urls:
        log.info(f'scrapping url {item+1}, {urls.index(item)}th of {len(urls)}')
        tag = item[32:len(item) - 6]
        dict_of_quotes[tag] = sc.parse_phrases(item)
    sc.write_phrases_to_txt(dict_of_quotes)
    log.info('all done')

if __name__ == '__main__':
    main()
