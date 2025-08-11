import typing

import bs4
import requests
from rignak.src.logging_utils import logger

from src.chair import get_chairs, Chair
from src.config import Config
from src.cours import Cours


def get_lines(chairs: typing.List[Chair]) -> typing.List[str]:
    lines = []
    logger.set_iterator(len(chairs))

    for chair in chairs:
        logger.iterate(f"{chair.name}:")
        index = 0
        logged_line = ""
        for index, card in enumerate(chair.get_cards()):
            cours = Cours()
            try:
                cours.initialize_from_card(card)
            except requests.RequestException:
                logger(f"{index} - NOK: {cours.chair} - #{index}")
            else:
                logged_line = f"{index} - {cours.chair} - {cours.enseignement} - {cours.name}"
                if not index:
                    logger(logged_line)
                elif index == 1:
                    logger('...')

                timestring = cours.time.isoformat().split('T')[0]
                data = (cours.chair, cours.enseignement, timestring, cours.name, cours.medial_url)
                lines.append("\t".join(data))
        if index:
            logger(logged_line)

        with open(Config.COURS_LIST_FILE, 'w') as file:
            file.write("\n".join(lines[::-1]))
    return lines


def main() -> None:
    chairs = get_chairs()
    get_lines(chairs)


if __name__ == "__main__":
    main()
