import datetime
import typing
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse, parse_qs

import bs4
from rignak.src.lazy_property import LazyProperty
from rignak.src.logging_utils import logger

from src.config import Config
from src.utils import get_soup


@dataclass
class Cours:
    url: typing.Optional[str] = None
    _medial_url : typing.Optional[str] = None
    _time: typing.Optional[datetime.datetime] = None

    _name: typing.Optional[str] = None
    _enseignement: typing.Optional[str] = None
    _chair: typing.Optional[str] = None

    _soup: typing.Optional[bs4.BeautifulSoup] = None
    _system_breadcrumbs: typing.Optional[bs4.BeautifulSoup] = None

    def initialize_from_card(self, card: bs4.Any) -> None:
        link_tag = card.find('a')
        if link_tag and link_tag.has_attr('href'):
            self.url = urljoin(Config.URL, link_tag['href'][3:])

    @LazyProperty
    def soup(self) -> bs4.BeautifulSoup:
        if self.url is None:
            raise ValueError("URL for this course has not been set.")

        soup = get_soup(self.url)
        return soup

    @LazyProperty
    def system_breadcrumbs(self) -> bs4.BeautifulSoup:
        breadcrumb = self.soup.find('nav', class_='breadcrumb')
        assert breadcrumb is not None, "No breadcrumb for this course?"
        return breadcrumb

    @LazyProperty
    def time(self) -> datetime.datetime:
        first_datetime_node = self.soup.find('time')
        return datetime.datetime.fromisoformat(first_datetime_node.get('datetime'))


    @LazyProperty
    def name(self) -> str:
        return self.system_breadcrumbs.find_all('li')[-1].text.strip()

    @LazyProperty
    def enseignement(self) -> str:
        return self.system_breadcrumbs.find_all('li')[-2].text.strip()

    @LazyProperty
    def chair(self) -> str:
        return self.system_breadcrumbs.find_all('li')[-4].text.strip()

    @LazyProperty
    def medial_url(self) -> str:
        media_url = ""

        iframe = self.soup.find('iframe', src=lambda s: s and 'oembed' in s)
        if iframe and ('youtube' in iframe['src'] or 'youtu.be' in iframe['src']):
            oembed_url = urljoin(self.url, iframe['src'])
            parsed_oembed_url = urlparse(oembed_url)
            query_params = parse_qs(parsed_oembed_url.query)
            if 'url' in query_params:
                media_url = query_params['url'][0]

        if not media_url:
            audio_link = self.soup.find('audio').find('source')
            if audio_link and audio_link.has_attr('src'):
                media_url = audio_link['src']
        return media_url