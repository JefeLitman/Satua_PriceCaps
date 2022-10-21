"""File containing the section 2 (market) configuration param of players
Version: 1.4
Made By: Edgar RP
"""
from otree.api import *
from utils import creating_session, set_players_results, get_price

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_2_market'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 8

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    seller_1_ask = models.IntegerField()
    seller_2_ask = models.IntegerField()
    seller_3_ask = models.IntegerField()
    seller_4_ask = models.IntegerField()

class Player(BasePlayer):
    winner_round = models.StringField()
    winner_section = models.StringField()
    treatment = models.StringField()
    bid_value = models.IntegerField()
    bid_accepted = models.BooleanField()
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
            fmi = player.session.config["treatment_FMI"],
            pce = player.session.config["treatment_PCE"],
            chosen_one = player.chosen_player,
            max_price = player.session.config["max_price"]
        )
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.session.config["treatment_PCE"]:
            player.participant.section_setting = True
        else:
            player.participant.section_setting = False

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
            pce = player.session.config["treatment_PCE"],
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
            pce = player.session.config["treatment_PCE"],
            chosen_one = player.chosen_player,
            max_price = player.session.config["max_price"]
        )

class wait_for_members(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and not player.session.config["treatment_FMI"]
    
    @staticmethod
    def after_all_players_arrive(group):
        set_players_results(group, 2, group.round_number)

class O004_mercado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and not player.session.config["treatment_FMI"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            seccion = 2,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS,
            valor=player.bid_value,
        )

class O005_resultado(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and not player.session.config["treatment_FMI"]

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        return dict(
            grupo = player.group_id,
            seccion = 2,
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
        return player.participant.consentimiento and player.round_number == C.NUM_ROUNDS and not player.session.config["treatment_FMI"]

    @staticmethod
    def vars_for_template(player):
        price = get_price(player)
        compras = sum([p.bid_accepted for p in player.in_all_rounds()])
        return dict(
            seccion = 2,
            total_periodos = C.NUM_ROUNDS,
            precio = price,
            compras = compras
        )

class O007_postexpectativa(Page):
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
            fmi = player.session.config["treatment_FMI"],
            max_price = player.session.config["max_price"]
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
        player.participant.chosen_player = player.chosen_player
        if player.chosen_player:
            player.participant.section_setting = player.section_3_setting
            for p in player.get_others_in_group():
                p.participant.section_setting = player.section_3_setting

page_sequence = [
    O001_informacion, 
    O002_preexpectativa,
    O003_decision,
    wait_for_members,
    O004_mercado,
    O005_resultado,
    O006_historial,
    O007_postexpectativa
]
