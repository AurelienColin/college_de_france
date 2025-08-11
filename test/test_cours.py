import datetime

import pytest

from src.config import Config
from src.cours import Cours


@pytest.fixture(scope="module")
def cours_with_video() -> Cours:
    cours = Cours(url=f"{Config.URL}/agenda/cours"
                      f"/dieu-en-guerre-recits-de-conquete-dans-le-livre-de-josue"
                      f"/differents-recits-de-conquete-jos-7-11")
    return cours

@pytest.fixture(scope="module")
def cours_with_audio() -> Cours:

    cours = Cours(url=f"{Config.URL}/agenda/lecture"
                      f"/the-palestine-question-from-1954"
                      f"/la-question-de-palestine-partir-de-1954-10")
    return cours

def test_cours_time(cours_with_video) -> None:
    assert cours_with_video.time == datetime.datetime.fromisoformat("2025-04-03T14:00:00Z")

def test_cours_chair(cours_with_video) -> None:
    assert cours_with_video.chair == "Thomas Römer, chaire Milieux bibliques"

def test_cours_enseignement(cours_with_video) -> None:
    assert cours_with_video.enseignement == "Dieu en guerre : récits de conquête dans le livre de Josué"

def test_cours_name(cours_with_video) -> None:
    assert cours_with_video.name == "Différents récits de conquête (Jos 7–11)"

def test_cours_video(cours_with_video) -> None:
    assert cours_with_video.medial_url == "https://youtu.be/0i6J9PkRQ_0"

def test_cours_audio(cours_with_audio) -> None:
    assert cours_with_audio.medial_url == ("https://www.college-de-france.fr"
                                           "/audio/henry-laurens/2007/1cours-henry-laurens.mp3")