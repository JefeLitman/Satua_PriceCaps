"""File containing the general and payments information for players
Version: 1.4
Made By: Edgar RP
"""

import random
from otree.api import *
from utils import set_experiment_params

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'informacion'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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
class O001_general(Page):
    pass
    

class O002_pago(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            points_4_cash = int(player.session.config["real_world_currency_per_point"]),
            fee = int(player.session.config["participation_fee"]),
            fmi=player.session.config["treatment_FMI"]
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.consentimiento = True
        player.participant.section_setting = None
        set_experiment_params(player)


page_sequence = [O001_general, O002_pago]
