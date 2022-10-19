"""File containing utilities functions for every market section in the whole app
Version: 1.5
Made By: Edgar RP
"""

import random

def set_experiment_params(player):
    player.winner_section = str(player.session.winner_section)
    player.winner_round = str(player.session.winner_round)
    if player.session.config["treatment_FME"]:
        player.treatment = "FME"    
    elif player.session.config["treatment_FMI"]:
        player.treatment = "FMI"
    else:
        player.treatment = "PCE"

def set_chosen_player(group):
    players = group.get_players()
    randomized = random.sample(players, len(players))
    randomized[0].chosen_player = True
    for p in randomized[1:]:
        p.chosen_player = False

def set_group_asks_bids(group):
    asks = [int(i) for i in group.session.config["seller_asks"].split(",")]
    for j in range(1, 5):
        setattr(group, "seller_{}_ask".format(j), asks[j-1])
    bids = [int(i) for i in group.session.config["players_bids"].split(",")]
    bids_randomized = random.sample(bids, k=len(bids))
    for i, p in enumerate(group.get_players()):
        p.bid_value = bids_randomized[i]

def get_price(player):
    asks = [int(i) for i in player.session.config["seller_asks"].split(",")]
    if player.participant.section_setting != None:
        if player.participant.section_setting:
            return max(asks)
        else:
            return player.session.config["max_price"]
    else:
        if player.session.config["treatment_PCE"]:
            return player.session.config["max_price"]
        else:
            return max(asks)

def set_players_results(group, section, round_number):
    asks = sorted([int(i) for i in group.session.config["seller_asks"].split(",")], reverse=True)
    bids = sorted(group.get_players(), key=lambda p: p.bid_value)
    for i, p in enumerate(bids):
        price = get_price(p)
        p.bid_accepted = p.bid_value >= asks[i] and asks[i] <= price
        if section == p.session.winner_section and round_number == p.session.winner_round:
            if p.bid_accepted:
                p.payoff = p.bid_value - price

def creating_session(subsession):
    if subsession.round_number == 1:
        #subsession.group_randomly()
        for g in subsession.get_groups():
            p = g.get_players()[0]
            try:
                if p.field_maybe_none("chosen_player") == None:
                    set_chosen_player(g)
            except AttributeError:
                pass
    else:
        subsession.group_like_round(1)
        for p in subsession.get_players():
            try:
                if p.field_maybe_none("chosen_player") == None:
                    p.chosen_player = p.in_round(1).chosen_player
            except AttributeError:
                pass
            
    for g in subsession.get_groups():
        set_group_asks_bids(g)
        for p in g.get_players():
            set_experiment_params(p)
