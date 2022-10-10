"""File containing the consent pages for the players
Version: 1.4
Made By: Edgar RP
"""
import random
from utils_simple import set_experiment_params
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
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()

# PAGES
class O001_consent(Page):
    form_model = 'player'
    form_fields = ['accepted']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.consentimiento = player.accepted
        random.seed(player.session.config["seed"]) #Implement the seed to replicate when creating sessions
        if player.session.config["treatment_FMI"]:
            sections = [1, 3, 4, 5, 6]
        else:
            sections = [1, 2, 3, 4, 5, 6]
        if player.session.config["name"].lower() == "Precios_Maximos_Full".lower():
            player.participant.winner_round = random.choice(range(1, 41))
        else:
            player.participant.winner_round = random.choice(range(1, 9))
        player.participant.winner_section = random.choice(sections)
        set_experiment_params(player)

page_sequence = [O001_consent]
