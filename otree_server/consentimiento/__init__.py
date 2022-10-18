"""File containing the consent pages for the players
Version: 1.8
Made By: Edgar RP
"""
import random
from utils import set_experiment_params
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

def creating_session(subsession):
    if (len(subsession.get_players()) / 4) % 2 != 0:
        raise AssertionError("The quantity of players must have an even number of groups with 4 player per group.")
    treatments = (subsession.session.config["treatment_FME"], subsession.session.config["treatment_FMI"], subsession.session.config["treatment_PCE"])
    if sum(treatments) != 1:
        raise AssertionError("You need to chose only one treatment for the session to start.")
    if len(subsession.session.config["seller_asks"].split(",")) != len(subsession.session.config["players_bids"].split(",")) != 4:
        raise AssertionError("The quantity of seller asks and player bids must be equal to 4 each.")
    random.seed(subsession.session.config["seed"]) #Implement the seed to replicate when creating sessions
    if subsession.session.config["treatment_FMI"]:
        sections = [1, 3, 4, 5, 6]
    else:
        sections = [1, 2, 3, 4, 5, 6]
    subsession.session.winner_section = random.choice(sections)
    if subsession.session.winner_section < 5:
        subsession.session.winner_round = random.choice(range(1, 9))
    else:
        subsession.session.winner_round = 1

# PAGES
class O001_consent(Page):
    form_model = 'player'
    form_fields = ['accepted']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.consentimiento = player.accepted
        player.participant.section_setting = None
        player.participant.chosen_player = None
        set_experiment_params(player)

page_sequence = [O001_consent]
