"""File containing the general and payments information for players
Version: 1.0
Made By: Edgar RP
"""
from otree.api import *


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
    pass


# PAGES
class O001_general(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento
    

class O002_pago(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento
        
    @staticmethod
    def vars_for_template(player):
        return dict(
            fmi=player.session.config["treatment_FMI"]
        )


page_sequence = [O001_general, O002_pago]
