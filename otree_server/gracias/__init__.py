"""File containing the gracias pages for the players
Version: 1.3
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
        total_payment = player.participant.payoff_plus_participation_fee()
        return dict(
            p_id = player.participant.label,
            aplica_ronda = player.session.winner_section not in [5, 6],
            seccion = player.session.winner_section,
            ronda = player.session.winner_round,
            fee = int(player.session.config["participation_fee"]),
            ganancias = int(total_payment - player.session.config["participation_fee"]),
            ganancias_totales = int(total_payment)
        )

page_sequence = [O001_gracias]
