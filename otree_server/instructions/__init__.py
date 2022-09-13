"""File containing the responses to be saved as instructions section
Version: 0.1
Made By: Edgar RP
"""
from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class general(Page):
    @staticmethod
    def is_displayed(player):
        # print(player.session.code)
        # print(player.group_id)
        # print(player.id_in_group)
        return True

class payments(Page):
    pass


page_sequence = [general, payments]
