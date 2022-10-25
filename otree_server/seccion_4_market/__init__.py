"""File containing the section 4 (market) configuration param of players
Version: 1.5
Made By: Edgar RP
"""
import numpy as np
from otree.api import *
from utils import creating_session, set_players_results, get_price

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_4_market'
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

# PAGES
class O001_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            decision = player.participant.section_setting,
            max_price = player.session.config["max_price"]
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def after_all_players_arrive(group):
        set_players_results(group, 4, group.round_number)

class O002_mercado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            seccion = 4,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS,
            valor=player.bid_value,
        )

class O003_resultado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento 

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        return dict(
            grupo = player.group_id,
            seccion = 4,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS,
            valor = player.bid_value,
            aceptada = "Sí" if player.bid_accepted else "No",
            precio = price,
            ganancia = player.bid_value - price if player.bid_accepted else 0
        )

class O004_historial(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        compras = sum([p.bid_accepted for p in player.in_all_rounds()])
        (earnings_1, earnings_2), (quantity_1, quantity_2) = np.unique([p.earnings for p in player.in_all_rounds()], return_counts=1)
        return dict(
            seccion = 4,
            total_periodos = C.NUM_ROUNDS,
            precio = price,
            compras = compras,
            earnings_1 = earnings_1,
            earnings_2 = earnings_2,
            quantity_1 = quantity_1,
            quantity_2 = quantity_2
        )

page_sequence = [
    O001_informacion, 
    wait_for_members,
    O002_mercado,
    O003_resultado,
    O004_historial
]
