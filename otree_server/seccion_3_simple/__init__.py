"""File containing the section 3 for simple version configuration of players
Version: 1.1
Made By: Edgar RP
"""
from otree.api import *
from utils_simple import creating_session, player_bid

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_3_simple'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 8

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    seller_1_ask = models.IntegerField()
    seller_2_ask = models.IntegerField()
    seller_3_ask = models.IntegerField()
    seller_4_ask = models.IntegerField()
    seller_5_ask = models.IntegerField()

class Player(BasePlayer):
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    bid_value = models.IntegerField()
    enter_bid = models.BooleanField()
    chosen_player = models.BooleanField()
    section_4_setting = models.BooleanField()

# PAGES
class O001_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

class O002_decision(Page):
    form_model = 'player'
    form_fields = ['section_4_setting']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            fmi = player.session.config["treatment_FMI"],
            chosen_one = player.chosen_player
        )

class O003_aviso(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            decision = player.participant.section_3_setting,
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

class O004_mercado(Page):
    form_model = 'player'
    form_fields = ['enter_bid']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["time_per_trading_period"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS,
            valor=player.bid_value,
        )

    @staticmethod
    def live_method(player, data):
        entered = data["enter_bid"]
        bid_result = player_bid(player, entered, 3)
        return {player.id_in_group: bid_result}

    @staticmethod
    def before_next_page(player, timeout_happened):
        player_bid(player, player.enter_bid, 3)
        if player.round_number > 1:
            player.section_4_setting = player.in_round(1).section_4_setting
        else:
            if player.chosen_player:
                player.participant.section_4_setting = player.section_4_setting
                for p in player.get_others_in_group():
                    p.participant.section_4_setting = player.section_4_setting

page_sequence = [
    O001_informacion, 
    O002_decision,
    O003_aviso,
    wait_for_members,
    O004_mercado
]
