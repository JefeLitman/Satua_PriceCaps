"""File containing the gracias pages for the players
Version: 1.1
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
    @staticmethod
    def vars_for_template(player):
        return dict(
            p_id = "SAMPLE_ID",
            aplica_ronda = player.session.winner_section not in [5, 6],
            seccion = player.session.winner_section,
            ronda = player.session.winner_round,
            fee = int(player.session.config["participation_fee"]),
            ganancias = int(player.participant.payoff - player.session.config["participation_fee"]),
            ganancias_totales = int(player.participant.payoff)
        )

page_sequence = [O001_gracias]
