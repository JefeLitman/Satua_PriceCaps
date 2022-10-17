"""File containing the section 1 (market) configuration param of players
Version: 1.5
Made By: Edgar RP
"""
from otree.api import *
from utils import creating_session, set_players_results, get_price

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_1_market'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    seller_1_ask = models.IntegerField()
    seller_2_ask = models.IntegerField()
    seller_3_ask = models.IntegerField()
    seller_4_ask = models.IntegerField()

class Player(BasePlayer):
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

# PAGES
class O001_instrucciones(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

class O002_resumen(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 1

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
            pce = player.session.config["treatment_PCE"],
            max_price = player.session.config["max_price"]
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento

    @staticmethod
    def after_all_players_arrive(group):
        if group.round_number > 2:
            set_players_results(group, 1, group.round_number - 2)
        else:
            set_players_results(group, 1, 0)

class O005_practica(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number <= 2

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            seccion = 1,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS - 8,
            valor=player.bid_value,
        )

class O006_resul_practica(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number <= 2

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        return dict(
            grupo = player.group_id,
            seccion = 1,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS - 8,
            valor = player.bid_value,
            aceptada = "Si" if player.bid_accepted else "No",
            precio = price,
            ganancia = player.bid_value - price if player.bid_accepted else 0
        )

class O007_informacion(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 3

    @staticmethod
    def vars_for_template(player):
        return dict(
            pce = player.session.config["treatment_PCE"],
            max_price = player.session.config["max_price"]
        )

class O008_mercado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number >= 3

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            seccion = 1,
            periodo = player.round_number - 2,
            total_periodos = C.NUM_ROUNDS - 2,
            valor=player.bid_value,
        )

class O009_resultado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number >= 3

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        return dict(
            grupo = player.group_id,
            seccion = 1,
            periodo = player.round_number - 2,
            total_periodos = C.NUM_ROUNDS - 2,
            valor = player.bid_value,
            aceptada = "Si" if player.bid_accepted else "No",
            precio = price,
            ganancia = player.bid_value - price if player.bid_accepted else 0
        )

class O010_historial(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number in [2, C.NUM_ROUNDS]

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        if player.round_number >= 3:
            total = C.NUM_ROUNDS - 2
            compras = sum([p.bid_accepted for p in player.in_rounds(3,10)])
        else:
            total = C.NUM_ROUNDS - 8
            compras = sum([p.bid_accepted for p in player.in_rounds(1,2)])
        return dict(
            seccion = 1,
            total_periodos = total,
            precio = price,
            compras = compras
        )

class O011_instr_expectativas(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS

class O012_expectativa(Page):
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
    def before_next_page(player, timeout_happened):
        player.participant.section_setting = None
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
    O007_informacion,
    wait_for_members,
    O005_practica,
    O006_resul_practica,
    O008_mercado,
    O009_resultado,
    O010_historial,
    O011_instr_expectativas,
    O012_expectativa
]
