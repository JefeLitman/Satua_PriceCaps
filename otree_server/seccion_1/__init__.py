"""File containing the section 1 configuration for players
Version: 0.2
Made By: Edgar RP
"""
from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'seccion_1'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class O001_instrucciones(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

class O002_revision(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

page_sequence = [O001_instrucciones]
