import pytest

from src.chair import Chair, get_chairs
from src.config import Config
from src.cours import Cours


@pytest.fixture(scope="module")
def first_chair() -> Chair:
    chair = get_chairs()[0]
    assert chair.url == f"{Config.URL}/chaire/thomas-romer-milieux-bibliques-chaire-statutaire"
    return chair


def test_first_chair_name(first_chair: Chair) -> None:
    assert first_chair.name == "Milieux bibliques"


def test_first_chair_data_url(first_chair: Chair) -> None:
    assert first_chair.data_url == f"{Config.URL}/enseignements/audios-videos"


def test_first_chair_first_course(first_chair: Chair) -> None:
    cards = first_chair.get_cards()
    first_card = next(cards)

    first_course = Cours()
    first_course.initialize_from_card(first_card)
    assert first_course.medial_url
