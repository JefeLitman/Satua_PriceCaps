"""File containing the consent pages for the players
Version: 1.2
Made By: Edgar RP
"""
import random
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
        random.seed(player.session.config["seed"]) #Implement the seed to replicate when creating sessions
        sections = range(1,7) if player.session.config["treatment_FMI"] else range(1,6)
        player.participant.winner_section = random.choice(sections)
        player.participant.winner_round = random.choice(range(1, 41))

page_sequence = [O001_consent]
