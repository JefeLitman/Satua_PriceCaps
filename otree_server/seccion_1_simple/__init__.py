"""File containing the section 1 for simple version configuration of players
Version: 1.0
Made By: Edgar RP
"""
from utils_simple import *
from otree.api import *

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_1_simple'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    seller_1_ask = models.IntegerField()
    seller_2_ask = models.IntegerField()
    seller_3_ask = models.IntegerField()
    seller_4_ask = models.IntegerField()
    seller_5_ask = models.IntegerField()

class Player(BasePlayer):
    bid_value = models.IntegerField()
    enter_bid = models.BooleanField()
    expectation_0_units = models.IntegerField()
    expectation_1_units = models.IntegerField()
    expectation_2_units = models.IntegerField()
    expectation_3_units = models.IntegerField()
    expectation_4_units = models.IntegerField()

# PAGES
class wait_for_all(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_randomly()
        for g in subsession.get_groups():
            set_group_asks_bids(g)
    
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

class O001_instrucciones(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

class O002_revision(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            time=player.session.config["time_per_trading_period"],
        )

class O003_chequeo(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

class O004_info_practica(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            pce = not player.session.config["treatment_FMI"]
        )
class O005_practica(Page):
    form_model = 'player'
    form_fields = ['enter_bid']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number <= 2

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["time_per_practice_period"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS - 8,
            valor=player.bid_value,
        )

    @staticmethod
    def live_method(player, data):
        entered = data["enter_bid"]
        bid_result = player_bid(player, entered, 1)
        return {player.id_in_group: bid_result}

    @staticmethod
    def before_next_page(player, timeout_happened):
        player_bid(player, player.enter_bid, 1)

class O006_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 2

    @staticmethod
    def vars_for_template(player):
        return dict(
            pce = not player.session.config["treatment_FMI"]
        )

class O007_mercado(Page):
    form_model = 'player'
    form_fields = ['enter_bid']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number > 2

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["time_per_trading_period"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            periodo = player.round_number - 2,
            total_periodos = C.NUM_ROUNDS - 2,
            valor=player.bid_value,
        )

    @staticmethod
    def live_method(player, data):
        entered = data["enter_bid"]
        bid_result = player_bid(player, entered, 1)
        return {player.id_in_group: bid_result}

    @staticmethod
    def before_next_page(player, timeout_happened):
        player_bid(player, player.enter_bid, 1)

class O008_expectativa(Page):
    form_model = 'player'
    form_fields = [
        'expectation_0_units',
        'expectation_1_units',
        'expectation_2_units',
        'expectation_3_units',
        'expectation_4_units'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        for p in player.in_previous_rounds():
            p.expectation_0_units = player.expectation_0_units
            p.expectation_1_units = player.expectation_1_units
            p.expectation_2_units = player.expectation_2_units
            p.expectation_3_units = player.expectation_3_units
            p.expectation_4_units = player.expectation_4_units

page_sequence = [
    wait_for_all,
    O001_instrucciones, 
    O002_revision, 
    O003_chequeo,
    O004_info_practica,
    O005_practica,
    O006_informacion,
    O007_mercado,
    O008_expectativa
]
