"""File containing utilities functions for every section with bid in the whole app
Version: 1.1
Made By: Edgar RP
"""

import random

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
    elif p > 0.75:
        sufix = group.session.config["increase_ask_by"]
    else:
        sufix = 0
    for j in sellers:
        final_value = values[j-1] + sufix
        if not group.session.config["treatment_FMI"] and final_value > 7:
            final_value = 7
        setattr(group, "seller_{}_ask".format(j), final_value)

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

def player_bid(player, value, section):
    player.bid_value = int(value)
    price = get_price(player.group)
    accepted = int(value) >= price
    if section == player.participant.winner_section and player.round_number == player.participant.winner_round:
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