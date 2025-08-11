import typing
from dataclasses import dataclass
from urllib.parse import urljoin

import bs4
import requests
from rignak.src.lazy_property import LazyProperty
from rignak.src.logging_utils import logger

from src.config import Config
from src.utils import get_soup


@dataclass
class Chair:
    url: str

    _name: typing.Optional[str] = None
    _data_url: typing.Optional[typing.Tuple[str, ...]] = None

    _soup: typing.Optional[typing.Union[bool, bs4.BeautifulSoup]] = None

    @LazyProperty
    def soup(self) -> typing.Union[bool, bs4.BeautifulSoup]:
        soup = False
        try:
            soup = get_soup(self.url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching chair page {self.url}: {e}")
        return soup

    @LazyProperty
    def name(self) -> str:
        if not self.soup:
            raise ValueError(f"Chair URL incorrectly parsed. Unable to find name.")

        h1 = self.soup.find('h1')
        if h1:
            name = ' '.join(h1.text.split())
        else:
            name = self.soup.title.string.strip()
        return name

    @LazyProperty
    def data_url(self) -> str:
        if not self.soup:
            raise ValueError(f"Chair URL incorrectly parsed. Unable to find resources.")

        data_url = ""
        link = self.soup.find_all('a', string="Audios & vidéos")[-2]
        if link and link.has_attr('href'):
            data_url = urljoin(self.url, link['href'])  + "&f[1]=type%3A4741"
        return data_url

    def get_cards(self) -> bs4.Any:
        for index in range(5):
            url = self.data_url + f"&page={index}"
            try:
                soup = get_soup(url)
                cards = soup.select('article.node--view-mode-audiovisual')
                if len(cards) == 0:
                    break
                for card in cards:
                    yield card

            except requests.exceptions.RequestException as e:
                logger(f"Error scraping page `{url}`: `{e}`")



def get_chairs() -> typing.List[Chair]:
    chairs: typing.List[Chair] = []
    with open(Config.CHAIRES_LIST_FILE, 'r') as file:
        for line in file.readlines():
            url = line.strip()
            if url:
                chair = Chair(f"{Config.URL}/chaire/{url}")
                chairs.append(chair)
    return chairs
