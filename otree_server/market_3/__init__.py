"""File containing the market_3 section configuration param of players
Version: 1.7
Made By: Edgar RP
"""
import numpy as np
from otree.api import *
from utils import creating_session, set_players_results, get_price

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'market_3'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 8

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    group_id = models.IntegerField()
    seller_1_ask = models.IntegerField()
    seller_2_ask = models.IntegerField()
    seller_3_ask = models.IntegerField()
    seller_4_ask = models.IntegerField()

class Player(BasePlayer):
    earnings = models.CurrencyField()
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    bid_value = models.IntegerField()
    bid_accepted = models.BooleanField()
    chosen_player = models.BooleanField()
    section_4_setting = models.BooleanField()

# PAGES
class O001_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number + 2,
            init_seccion = player.session.market_initial_number,
            second_seccion = player.session.market_initial_number + 1,
            next_seccion = player.session.market_initial_number + 3,
            pce = player.session.config["treatment_PCE"],
            max_price = player.session.config["max_price"]
        )

class O002_decision(Page):
    form_model = 'player'
    form_fields = ['section_4_setting']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number + 2,
            init_seccion = player.session.market_initial_number,
            second_seccion = player.session.market_initial_number + 1,
            next_seccion = player.session.market_initial_number + 3,
            pce = player.session.config["treatment_PCE"],
            chosen_one = player.participant.chosen_player,
            max_price = player.session.config["max_price"]
        )

class O003_aviso(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number + 2,
            decision = player.participant.section_setting,
            max_price = player.session.config["max_price"]
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def after_all_players_arrive(group):
        seccion = group.session.market_initial_number + 2
        set_players_results(group, seccion, group.round_number)

class O004_mercado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group.group_id,
            seccion = player.session.market_initial_number + 2,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS,
            valor=player.bid_value,
        )

class O005_resultado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento 

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        return dict(
            grupo = player.group.group_id,
            seccion = player.session.market_initial_number + 2,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS,
            valor = player.bid_value,
            aceptada = "Sí" if player.bid_accepted else "No",
            precio = price,
            ganancia = player.bid_value - price if player.bid_accepted else 0
        )

class O006_historial(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        compras = sum([p.bid_accepted for p in player.in_all_rounds()])
        (earnings_1, earnings_2), (quantity_1, quantity_2) = np.unique([p.earnings for p in player.in_all_rounds()], return_counts=1)
        return dict(
            seccion = player.session.market_initial_number + 2,
            total_periodos = C.NUM_ROUNDS,
            precio = price,
            compras = compras,
            earnings_1 = earnings_1,
            earnings_2 = earnings_2,
            quantity_1 = quantity_1,
            quantity_2 = quantity_2
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.section_4_setting = player.in_round(1).section_4_setting
        player.chosen_player = player.participant.chosen_player
        for p in player.in_previous_rounds():
            p.section_4_setting = player.in_round(1).section_4_setting
            p.chosen_player = player.participant.chosen_player
        if player.chosen_player:
            player.participant.section_setting = player.section_4_setting
            for p in player.get_others_in_group():
                p.participant.section_setting = player.section_4_setting

page_sequence = [
    O001_informacion, 
    O002_decision,
    O003_aviso,
    wait_for_members,
    O004_mercado,
    O005_resultado,
    O006_historial
]
