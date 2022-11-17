"""File containing the market_1 section configuration param of players
Version: 2.2
Made By: Edgar RP
"""
import numpy as np
from otree.api import *
from utils import creating_session, set_players_results, get_price

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'market_1'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    practice_rounds = 2

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
    bid_value = models.IntegerField()
    bid_accepted = models.BooleanField()
    expectation_0_after = models.IntegerField()
    expectation_1_after = models.IntegerField()
    expectation_2_after = models.IntegerField()
    expectation_3_after = models.IntegerField()
    expectation_4_after = models.IntegerField()
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    checking_1_history = models.StringField()
    checking_2_history = models.StringField()
    checking_3_history = models.StringField()
    checking_4_history = models.StringField()

# PAGES
class O001_instrucciones(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number
        )

class O002_resumen(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number
        )

class O003_chequeo(Page):
    form_model = 'player'
    form_fields = [
        'checking_1_history',
        'checking_2_history',
        'checking_3_history',
        'checking_4_history'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number
        )

class O004_info_practica(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number,
            pce = player.session.config["treatment_PCE"],
            max_price = player.session.config["max_price"]
        )

class O005_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 3

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number,
            pce = player.session.config["treatment_PCE"],
            max_price = player.session.config["max_price"]
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def after_all_players_arrive(group):
        section = group.session.market_initial_number
        if group.round_number > 2:
            set_players_results(group, section, group.round_number - C.practice_rounds)
        else:
            set_players_results(group, section, 0)

class O006_mercado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        if player.round_number >= 3:
            head = "períodos reales"
            total = C.NUM_ROUNDS - C.practice_rounds
            current_round = player.round_number - C.practice_rounds
        else:
            head = "períodos de práctica"
            total = C.practice_rounds
            current_round = player.round_number
        return dict(
            header = head,
            grupo = player.group.group_id,
            seccion = player.session.market_initial_number,
            periodo = current_round,
            total_periodos = total,
            valor=player.bid_value,
        )

class O007_resultado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        if player.round_number >= 3:
            head = "períodos reales"
            total = C.NUM_ROUNDS - C.practice_rounds
            current_round = player.round_number - C.practice_rounds
        else:
            head = "períodos de práctica"
            total = C.practice_rounds
            current_round = player.round_number
        return dict(
            header = head,
            grupo = player.group.group_id,
            seccion = player.session.market_initial_number,
            periodo = current_round,
            total_periodos = total,
            valor = player.bid_value,
            aceptada = "Sí" if player.bid_accepted else "No",
            precio = price,
            ganancia = player.bid_value - price if player.bid_accepted else 0
        )

class O008_historial(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number in [2, C.NUM_ROUNDS]

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        if player.round_number >= 3:
            head = player.session.market_initial_number
            section = player.session.market_initial_number
            total = C.NUM_ROUNDS - C.practice_rounds
            compras = sum([p.bid_accepted for p in player.in_rounds(3,10)])
            (earnings_1, earnings_2), (quantity_1, quantity_2) = np.unique([p.earnings for p in player.in_rounds(3,10)], return_counts=1)
        else:
            head = "de práctica"
            section = "de práctica"
            total = C.NUM_ROUNDS - 8
            compras = sum([p.bid_accepted for p in player.in_rounds(1,2)])
            (earnings_1, earnings_2), (quantity_1, quantity_2) = np.unique([p.earnings for p in player.in_rounds(1,2)], return_counts=1)
        return dict(
            header = head,
            seccion = section,
            total_periodos = total,
            precio = price,
            compras = compras,
            earnings_1 = earnings_1,
            earnings_2 = earnings_2,
            quantity_1 = quantity_1,
            quantity_2 = quantity_2
        )

class O009_instr_expectativas(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number
        )

class O010_expectativa(Page):
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
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        return dict(
            seccion = player.session.market_initial_number
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.section_setting = None
        for i in range(1,5):
            attr = "checking_{}_history".format(i)
            value = getattr(player.in_round(1), attr)
            for p in player.in_rounds(2, C.NUM_ROUNDS):
                setattr(p, attr, value)
        for p in player.in_previous_rounds():
            for i in range(5):
                attr = "expectation_{}_after".format(i)
                value = getattr(player, attr)
                setattr(p, attr, value)

page_sequence = [
    O001_instrucciones, 
    O002_resumen, 
    O003_chequeo,
    O004_info_practica,
    O005_informacion,
    wait_for_members,
    O006_mercado,
    O007_resultado,
    O008_historial,
    O009_instr_expectativas,
    O010_expectativa
]
