"""File containing the gracias pages for the players
Version: 1.4
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
class saving_participation(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        for player in group.get_players():
            with open("./participants_data/history.csv", "a") as history:
                history.write('\"{}\"'.format(player.participant.label) + "\n")

class O001_gracias(Page):
    @staticmethod
    def vars_for_template(player):
        total_payment = player.participant.payoff_plus_participation_fee()
        unique_round = [
            player.session.lottery_section_number, 
            player.session.assignation_section_number
        ]
        return dict(
            p_id = player.participant.label,
            aplica_ronda = player.session.winner_section not in unique_round,
            seccion = player.session.winner_section,
            ronda = player.session.winner_round,
            fee = int(player.session.config["participation_fee"]),
            ganancias = int(total_payment - player.session.config["participation_fee"]),
            ganancias_totales = int(total_payment)
        )

page_sequence = [saving_participation, O001_gracias]
