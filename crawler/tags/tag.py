from bs4 import BeautifulSoup


# Tags

anchor_tag = "a"

audio_tag = "audio"
image_tag = "img"
video_tag = "video"

script_tag = "script"


class Tag:

    def __init__(self, tag):
        self.tag = tag

    def get_tags(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find_all(self.tag)
        return tags

def _get_tags(html, tag):
    """

    :param html: html to parse
    :param tag: tag to search for
    :return: list
    """
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all(tag)
    return anchors


def get_anchors(html):
    """

    :param html: html to search
    :return: list
    """

    return _get_tags(html, anchor_tag)


def get_scripts(html, external_only=True):
    """

    :param html: html to search
    :param external_only: only find external scripts
    :return: list
    """
    tags = _get_tags(html, script_tag)

    if external_only:
        external_scripts = list()
        for tag in tags:
            if tag.get('src'):
                external_scripts.append(tag)

        return external_scripts

    return tags


def get_images(html):
    """

    :param html: html to search
    :return: list
    """
    return _get_tags(html, image_tag)
