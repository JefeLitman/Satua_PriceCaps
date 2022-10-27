"""File containing the section 6 (assignation) configuration param of players
Version: 1.5
Made By: Edgar RP
"""
from otree.api import *
import random
from utils import set_experiment_params, set_chosen_player, set_groups

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_6_assignation'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    group_id = models.IntegerField()

class Player(BasePlayer):
    earnings = models.CurrencyField()
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    group_designed = models.StringField()
    chosen_player = models.BooleanField()
    chosen_allocation = models.IntegerField()

def creating_session(subsession):
    set_groups(subsession)
    groups = subsession.get_groups()
    randomized_groups = random.sample(groups, len(groups))
    correspondence = randomized_groups[1:] + [randomized_groups[0]]
    
    for i, g in enumerate(randomized_groups):
        set_chosen_player(g)
        for p in g.get_players():
            p.group_designed = str(correspondence[i].group_id)
            set_experiment_params(p)
    
# PAGES
class O001_asignacion(Page):
    form_model = 'player'
    form_fields = ['chosen_allocation']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            my_group = player.group_id,
            other_group = player.group_designed
        )

class wait_for_all_groups(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        groups = [(g.group_id, g) for g in subsession.get_groups()]
        for p in subsession.get_players():
            if p.chosen_player:
                for g_id, g in groups:
                    if p.group_designed == str(g_id):
                        players = g.get_players()
                        randomized_players = random.sample(players, len(players))
                        if p.chosen_allocation == 1:
                            for i, o_p in enumerate(randomized_players):
                                if i < len(players) / 2:
                                    o_p.earnings = 3
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 3
                                else:
                                    o_p.earnings = 2
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 2
                        else:
                            for i, o_p in enumerate(randomized_players):
                                if i < len(players) / 2:
                                    o_p.earnings = 5
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 5
                                else:
                                    o_p.earnings = 0
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 0 
                        break

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento
class O002_resultado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            other_group = player.group_designed,
            puntos = player.earnings
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        with open("./participants_data/history.csv", "a") as history:
            history.write('\"{}\"'.format(player.participant.label) + "\n")
        

page_sequence = [
    O001_asignacion,
    wait_for_all_groups,
    O002_resultado
]
