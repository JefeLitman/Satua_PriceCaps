"""File containing the section 5 configuration of players
Version: 1.0
Made By: Edgar RP
"""
from otree.api import *
import random
from utils_simple import set_experiment_params

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_5'
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
    ticket_color = models.StringField()
    lotery_selection = models.IntegerField()

# PAGES
class wait_for_all_grouping(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        players = subsession.get_players()
        n_players = len(players)
        randomized_players = random.sample(players, n_players)
        for i, p in enumerate(randomized_players):
            if i < n_players // 2:
                p.ticket_color = "Roja"
            else:
                p.ticket_color = "Azul"
            set_experiment_params(p)
    
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

class O001_loteria(Page):
    form_model = 'player'
    form_fields = ['lotery_selection']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

page_sequence = [
    wait_for_all_grouping,
    O001_loteria
]
