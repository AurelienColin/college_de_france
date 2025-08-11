import os
from dataclasses import dataclass


@dataclass
class Config:
    URL: str = "https://www.college-de-france.fr/fr"
    ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RES_DIR: str = os.path.join(ROOT_DIR, "res")
    DOWNLOAD_DIR: str = os.path.join(ROOT_DIR, "downloads")

    CHAIRES_LIST_FILE: str = os.path.join(RES_DIR, "liste_des_chaires.txt")
    COURS_LIST_FILE: str = os.path.join(RES_DIR, "liste_des_cours.txt")
