"""File containing the consent pages for the players
Version: 1.1
Made By: Edgar RP
"""
from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'consentimiento'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    accepted = models.BooleanField()

# PAGES
class O001_consent(Page):
    form_model = 'player'
    form_fields = ['accepted']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.consentimiento = player.accepted


page_sequence = [O001_consent]