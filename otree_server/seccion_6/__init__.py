"""File containing the section 6 configuration of players
Version: 0.1
Made By: Edgar RP
"""
from otree.api import *
import random
from utils_simple import set_experiment_params, set_chosen_player

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_6'
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
    payment_asignation = models.IntegerField()

# PAGES
class wait_for_all_grouping(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        groups = subsession.get_groups()
        groups_ids = [i.group_id for i in groups]
        while True:
            randomized_ids = random.sample(groups_ids, len(groups_ids))
            if all(groups_ids[i] != randomized_ids[i] for i in range(len(groups_ids))):
                break
        for i, g in enumerate(groups):
            set_chosen_player(g)
            for p in g.get_players():
                p.group_designed = str(randomized_ids[i])
    
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

class O001_asignacion(Page):
    form_model = 'player'
    form_fields = ['payment_asignation']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            my_group = player.group_id,
            other_group = player.group_designed
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        ### Falta definir el payment aca
        set_experiment_params(player)

page_sequence = [
    wait_for_all_grouping,
    O001_asignacion
]
