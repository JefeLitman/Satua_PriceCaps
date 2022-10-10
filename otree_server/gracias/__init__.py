"""File containing the gracias pages for the players
Version: 1.0
Made By: Edgar RP
"""
from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'gracias'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

# PAGES
class O001_gracias(Page):
    pass

page_sequence = [O001_gracias]
