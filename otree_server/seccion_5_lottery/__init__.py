"""File containing the section 5 (lottery) configuration param of players
Version: 1.2
Made By: Edgar RP
"""
from otree.api import *
import random
from utils import set_experiment_params

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_5_lottery'
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

def creating_session(subsession):
    players = subsession.get_players()
    n_players = len(players)
    randomized_players = random.sample(players, n_players)
    for i, p in enumerate(randomized_players):
        if i < n_players // 2:
            p.ticket_color = "Roja"
        else:
            p.ticket_color = "Azul"
        set_experiment_params(p)

# PAGES
class O001_loteria(Page):
    form_model = 'player'
    form_fields = ['lotery_selection']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            roja = player.ticket_color.lower() == "roja"
        )

class O002_espera(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            roja = player.ticket_color.lower() == "roja",
            loteria_1 = player.lotery_selection == 1
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.session.winner_section == 5:
            if player.lotery_selection == 1:
                if player.session.comment.lower() == player.ticket_color.lower():
                    player.payoff = 3
                else:
                    player.payoff = 2
            else:
                if player.session.comment.lower() == player.ticket_color.lower():
                    player.payoff = 5

page_sequence = [
    O001_loteria,
    O002_espera
]
