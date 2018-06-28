import os
import uuid
from pathlib import Path

import requests
from requests.exceptions import MissingSchema

from .page import Page


class Crawler:

    def __init__(self, domain, output_dir):
        self.domain = domain
        self.output_dir = output_dir
        self.crawl_output_dir = ""

        self.urls_to_crawl = list()
        self.urls_crawled = list()
        self.images_saved = list()
        self.scripts_saved = list()

    def _create_job_directory(self):
        """
        Create a random directory for the crawl.
        :return: str: crawl directory
        """
        crawl_output_dir = self.output_dir + str(uuid.uuid4()) + '/'
        Path(crawl_output_dir).mkdir(parents=True, exist_ok=True)
        return crawl_output_dir

    def _save_file(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(str(content))

    def _print_job_status(self):
        print("{} page(s) to crawl. {} page(s) crawled.".format(len(self.urls_to_crawl), len(self.urls_crawled)))

    def _process(self, page):
        """
        Process the page's anchors, scripts and images.
        :param page:
        :return: None
        """
        # Process anchors
        if page.anchors:
            number_of_anchors = len(page.anchors)
            number_of_filtered_anchors = 0

            for anchor in page.anchors:
                if anchor.get('href'):

                    if anchor.get('href')[0] == '/':
                        anchor_path = page.url + anchor.get('href')
                    # TODO This'll miss sub domains.
                    elif anchor.get('href').startswith(self.domain):
                        anchor_path = anchor.get('href')

                    # Add the current path
                    if anchor_path not in self.urls_crawled and anchor_path not in self.urls_to_crawl:
                        self.urls_to_crawl.append(anchor_path)
                        number_of_filtered_anchors += 1

            print('\t{}/{} anchors saved.'.format(number_of_filtered_anchors, number_of_anchors))

        if page.scripts:
            # Save all external scripts.
            number_of_scripts = len(page.scripts)
            number_of_filtered_scripts = 0

            for script in page.scripts:
                # If the first character in the URL is a `/`, the file is on the current domain.
                # TODO This'll miss absolute paths.
                if script['src'][0] == '/':
                    script_url = self.domain + script['src']
                    if script_url not in self.scripts_saved:
                        response = requests.get(script_url)
                        if response.ok:
                            script_path = self.crawl_output_dir + script['src']
                            self._save_file(script_path, response.content)
                            self.scripts_saved = script_path
                            number_of_filtered_scripts += 1
            print('\t{}/{} scripts saved.'.format(number_of_filtered_scripts, number_of_scripts))

        if page.images:
            # Save all images
            number_of_images = len(page.images)
            number_of_filtered_images = 0

            for image in page.images:
                # TODO This is pulling in images that are NOT on the domain.
                try:
                    response = requests.get(image['src'])
                except MissingSchema as e:
                    print(e)

                image_path = self.crawl_output_dir + image['src']
                if image_path not in self.images_saved:
                    if response.ok:
                        self._save_file(image_path, response.content)
                        self.images_saved = image_path
                        number_of_filtered_images += 1

            print('\t{}/{} images saved.'.format(number_of_filtered_images, number_of_images))

    def crawl(self):
        """
        Crawl the domain.
        :return: None
        """

        # Create the directory structure for the domain.
        self.crawl_output_dir = self._create_job_directory()

        print('Starting crawl for domain: {}...'.format(self.domain))

        # Put the first url into the queue.
        self.urls_to_crawl.append(self.domain)

        # Process all child pages.
        while self.urls_to_crawl:

            page = Page(self.urls_to_crawl.pop(0))
            page.crawl()
            self._save_file(self.crawl_output_dir + page.url + '.html', page.html)
            self._process(page)
            self.urls_crawled.append(page.url)
            self._print_job_status()
