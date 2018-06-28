import os

from crawler.crawler import Crawler

url = os.getenv('URL')
output_dir = os.getenv('OUTPUT_DIR')

crawler = Crawler(url, output_dir)

crawler.crawl()
