"""File containing the section 1 configuration for players
Version: 0.4
Made By: Edgar RP
"""
import random
from otree.api import *

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'seccion_1'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 46

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    seller_1_ask = models.IntegerField()
    seller_2_ask = models.IntegerField()
    seller_3_ask = models.IntegerField()
    seller_4_ask = models.IntegerField()
    seller_5_ask = models.IntegerField()

class Player(BasePlayer):
    max_value = models.IntegerField()
    bid_value = models.IntegerField()
    bid_history = models.StringField()

# FUNCTIONS SECTION FOR CODE
def get_ask_generator(subsession):
    min_ask = subsession.session.config["min_ask"]
    if subsession.session.config["treatment_FMI"]:
        max_ask = subsession.session.config["max_ask"]
    else:
        max_ask = 7
    generator = lambda: random.randint(min_ask, max_ask)
    return generator

def set_group_asks(group, round_number):
    sellers = range(1,6)
    if round_number in [1, 7]:
        gen = get_ask_generator(group.subsession)
        values = [gen() for _ in sellers]
    else:
        if round_number < 7:
            values = [getattr(group.in_round(1), "seller_{}_ask".format(j)) for j in sellers]
        else:
            values = [getattr(group.in_round(7), "seller_{}_ask".format(j)) for j in sellers]
    # Add a random probability of 25% to increase/decrease the asks by sellers
    p = random.random()
    if p < 0.25: # Decrease
        sufix = -group.session.config["decrease_ask_by"]
    elif p > 0.25:
        sufix = group.session.config["increase_ask_by"]
    else:
        sufix = 0
    for j in sellers:
        setattr(group, "seller_{}_ask".format(j), values[j-1] + sufix)

def get_price(group):
    sellers = range(1,6)
    buyers = group.get_players()
    asks = sorted([getattr(group, "seller_{}_ask".format(i)) for i in sellers])
    bids = []
    for player in buyers:
        value = player.field_maybe_none("bid_value")
        if value == None:
            value = 0
        bids.append(value)
    bids = sorted(bids, reverse=True)
    for i in range(len(buyers) - 1, -1, -1):
        if bids[i] >= asks[i]:
            return asks[i]
    return asks[-1]

def set_player_values(player):
    player.max_value = random.randint(player.session.config["min_value"], player.session.config["max_value"])
    if not player.participant.consentimiento:
        player.bid_value = random.randint(1, player.max_value)
        player.bid_history = "Bot Player"

def player_bid(player, value):
    player.bid_value = int(value)
    price = get_price(player.group)
    accepted = int(value) >= price
    player.payoff = player.max_value - price if accepted else 0
    return {
        "bid": value, 
        "accepted": accepted,
        "price": price
    }

def add_history_value(player, value):
    history = player.field_maybe_none("bid_history")
    if history == None:
        values = []
    else:
        values = history.split("-")
    values.append(value)
    player.bid_history = "-".join([str(i) for i in values])

# PAGES
class wait_for_all(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        if subsession.round_number == 1:
            random.seed(subsession.session.config["seed"]) #Implement the seed to replicate when creating sessions
        subsession.group_randomly()
        for g in subsession.get_groups():
            set_group_asks(g, subsession.round_number)
        for p in subsession.get_players():
            set_player_values(p)
    
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

class O004_practica(Page):
    form_model = 'player'
    form_fields = ['bid_value']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number <= 6

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["time_per_practice_period"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            periodo = player.round_number,
            total_periodos = C.NUM_ROUNDS - 40,
            valor=player.max_value,
        )
    
    @staticmethod
    def js_vars(player):
        return dict(
            max_value=player.max_value
        )

    @staticmethod
    def live_method(player, data):
        value = data["value"]
        add_history_value(player, value)
        bid_result = player_bid(player, value)
        return {player.id_in_group: bid_result}

class O005_cambio(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number == 6

class O006_trading(Page):
    form_model = 'player'
    form_fields = ['bid_value']

    @staticmethod
    def is_displayed(player):
        return player.participant.consentimiento and player.round_number > 6

    @staticmethod
    def get_timeout_seconds(player):
        return player.session.config["time_per_trading_period"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            grupo = player.group_id,
            periodo = player.round_number - 6,
            total_periodos = C.NUM_ROUNDS - 6,
            valor=player.max_value,
        )
    
    @staticmethod
    def js_vars(player):
        return dict(
            max_value=player.max_value
        )

    @staticmethod
    def live_method(player, data):
        value = data["value"]
        add_history_value(player, value)
        bid_result = player_bid(player, value)
        return {player.id_in_group: bid_result}

page_sequence = [
    wait_for_all,
    O001_instrucciones, 
    O002_revision, 
    O003_chequeo,
    O004_practica,
    O005_cambio,
    O006_trading
]
