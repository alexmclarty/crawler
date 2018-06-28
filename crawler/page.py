import requests

from .tags.tag import get_anchors, get_scripts, get_images


class Page:
    """
    Represents a page to crawl.
    """

    def __init__(self, url):
        """
        :param url: str: url to crawl
        """
        self.url = url
        self.html = None
        self.anchors = None
        self.images = None
        self.scripts = None

    def _get_url(self):
        response = requests.get(self.url)
        if response.ok:
            self.html = response.content
            print('Crawled page at {}'.format(self.url))

    def _parse_html(self):
        anchors = get_anchors(self.html)
        self.anchors = anchors

        scripts = get_scripts(self.html)
        self.scripts = scripts

        images = get_images(self.html)
        self.images = images

    def crawl(self):
        """
        Crawl and parse the page.
        :return:
        """
        self._get_url()
        if self.html:
            self._parse_html()

