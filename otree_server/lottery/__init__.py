"""File containing the lottery section configuration param of players
Version: 1.5
Made By: Edgar RP
"""
from otree.api import *
import random
from utils import set_experiment_params

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'lottery'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    earnings = models.CurrencyField()
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    ticket_color = models.StringField()
    lottery_selection = models.IntegerField()

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
    form_fields = ['lottery_selection']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.lottery_section_number,
            roja = player.ticket_color.lower() == "roja"
        )

class O002_espera(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.lottery_section_number,
            roja = player.ticket_color.lower() == "roja",
            loteria_1 = player.lottery_selection == 1
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.lottery_selection == 1:
            if player.session.comment.lower() == player.ticket_color.lower():
                player.earnings = 3
            else:
                player.earnings = 2
        else:
            if player.session.comment.lower() == player.ticket_color.lower():
                player.earnings = 5
            else:
                player.earnings = 0
        if player.session.winner_section == player.session.lottery_section_number:
            player.payoff = player.earnings

page_sequence = [
    O001_loteria,
    O002_espera
]
