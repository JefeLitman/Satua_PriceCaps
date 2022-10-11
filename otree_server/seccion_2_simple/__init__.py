"""File containing the section 2 for simple version configuration of players
Version: 1.2
Made By: Edgar RP
"""
from otree.api import *
from utils_simple import creating_session, player_bid

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_2_simple'
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
    section_3_setting = models.BooleanField()
    expectation_0_before = models.IntegerField()
    expectation_1_before = models.IntegerField()
    expectation_2_before = models.IntegerField()
    expectation_3_before = models.IntegerField()
    expectation_4_before = models.IntegerField()
    expectation_0_after = models.IntegerField()
    expectation_1_after = models.IntegerField()
    expectation_2_after = models.IntegerField()
    expectation_3_after = models.IntegerField()
    expectation_4_after = models.IntegerField()

# PAGES
class O001_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            fmi = player.session.config["treatment_FMI"]
        )

class O002_preexpectativa(Page):
    form_model = 'player'
    form_fields = [
        'expectation_0_before',
        'expectation_1_before',
        'expectation_2_before',
        'expectation_3_before',
        'expectation_4_before'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            fmi = player.session.config["treatment_FMI"]
        )

class O003_decision(Page):
    form_model = 'player'
    form_fields = ['section_3_setting']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            fmi = player.session.config["treatment_FMI"],
            chosen_one = player.chosen_player
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and not player.session.config["treatment_FMI"]

class O004_mercado(Page):
    form_model = 'player'
    form_fields = ['enter_bid']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and not player.session.config["treatment_FMI"]

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
        bid_result = player_bid(player, entered, 2)
        return {player.id_in_group: bid_result}

    @staticmethod
    def before_next_page(player, timeout_happened):
        player_bid(player, player.enter_bid, 2)

class O005_postexpectativa(Page):
    form_model = 'player'
    form_fields = [
        'expectation_0_after',
        'expectation_1_after',
        'expectation_2_after',
        'expectation_3_after',
        'expectation_4_after'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 8

    @staticmethod
    def vars_for_template(player):
        return dict(
            fmi = player.session.config["treatment_FMI"]
        )
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.section_3_setting = player.in_round(1).section_3_setting
        for i in range(5):
            attr = "expectation_{}_before".format(i)
            value = getattr(player.in_round(1), attr)
            setattr(player, attr, value)
        for p in player.in_previous_rounds():
            for i in range(5):
                attr = "expectation_{}_after".format(i)
                value = getattr(player, attr)
                setattr(p, attr, value)
                attr = "expectation_{}_before".format(i)
                value = getattr(player.in_round(1), attr)
                setattr(p, attr, value)
            p.section_3_setting = player.in_round(1).section_3_setting
        if player.chosen_player:
            player.participant.section_3_setting = player.section_3_setting
            for p in player.get_others_in_group():
                p.participant.section_3_setting = player.section_3_setting

page_sequence = [
    O001_informacion, 
    O002_preexpectativa,
    O003_decision,
    wait_for_members,
    O004_mercado,
    O005_postexpectativa
]
