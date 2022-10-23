"""File containing the section 6 (assignation) configuration param of players
Version: 1.2
Made By: Edgar RP
"""
from otree.api import *
import random
from utils import set_experiment_params, set_chosen_player

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
    pass

class Player(BasePlayer):
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    group_designed = models.StringField()
    chosen_player = models.BooleanField()
    chosen_allocation = models.IntegerField()
    payment_received = models.IntegerField()

def creating_session(subsession):
    # Falta mantener la agrupacion igual que las secciones 1,2,3 y 4
    groups = subsession.get_groups()
    groups_ids = [(i, g.id) for i, g in enumerate(groups)]
    assigned_ids = random.sample(groups_ids, len(groups_ids))
    for index in range(0, len(assigned_ids), 2):
        g1 = groups[assigned_ids[index][0]]
        g_id_1 = assigned_ids[index][1]
        g2 = groups[assigned_ids[index + 1][0]]
        g_id_2 = assigned_ids[index + 1][1]
        set_chosen_player(g1)
        set_chosen_player(g2)
        for p in g1.get_players():
            p.group_designed = str(g_id_2)
            set_experiment_params(p)
        for p in g2.get_players():
            p.group_designed = str(g_id_1)
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
        groups = [(g.id, g) for g in subsession.get_groups()]
        for p in subsession.get_players():
            if p.chosen_player:
                for g_id, g in groups:
                    if p.group_designed == str(g_id):
                        players = g.get_players()
                        randomized_players = random.sample(players, len(players))
                        if p.chosen_allocation == 1:
                            for i, o_p in enumerate(randomized_players):
                                if i < len(players) / 2:
                                    o_p.payment_received = 3
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 3
                                else:
                                    o_p.payment_received = 2
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 2
                        else:
                            for i, o_p in enumerate(randomized_players):
                                if i < len(players) / 2:
                                    o_p.payment_received = 5
                                    if subsession.session.winner_section == 6:
                                        o_p.payoff = 5
                                else:
                                    o_p.payment_received = 0
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
            puntos = player.payment_received
        )
        

page_sequence = [
    O001_asignacion,
    wait_for_all_groups,
    O002_resultado
]
