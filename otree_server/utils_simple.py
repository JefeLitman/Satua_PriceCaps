"""File containing utilities functions for every simple section in the whole app
Version: 0.1
Made By: Edgar RP
"""

import random

def set_group_asks_bids(group):
    asks = [int(i) for i in group.session.config["seller_asks"].split(",")]
    for j in range(1, 6):
        setattr(group, "seller_{}_ask".format(j), asks[j-1])
    bids = [int(i) for i in group.session.config["players_max_bids"].split(",")]
    bids_randomized = random.sample(bids, k=len(bids))
    for i, p in enumerate(group.get_players()):
        p.bid_value = bids_randomized[i]
    
def get_price(group):
    asks = sorted([int(i) for i in group.session.config["seller_asks"].split(",")])
    bids = []
    for player in group.get_players():
        participated = player.field_maybe_none("enter_bid")
        if participated:
            bids.append(player.bid_value)
    bids = sorted(bids, reverse=True)
    max_ask = max(asks) if group.session.config["treatment_FMI"] else 7
    for i in range(len(bids) - 1, -1, -1):
        if bids[i] >= asks[i]:
            return asks[i] if asks[i] <= max_ask else max_ask
    return max_ask

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