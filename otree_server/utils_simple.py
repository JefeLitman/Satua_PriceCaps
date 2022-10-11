"""File containing utilities functions for every simple section in the whole app
Version: 1.2
Made By: Edgar RP
"""

import random

def set_experiment_params(player):
    player.winner_section = str(player.session.winner_section)
    player.winner_round = str(player.session.winner_round)
    player.treatment = "FMI" if player.session.config["treatment_FMI"] else "PCE"

def set_chosen_player(group):
    players = group.get_players()
    randomized = random.sample(players, len(players))
    randomized[0].chosen_player = True
    for p in randomized[1:]:
        p.chosen_player = False

def set_group_asks_bids(group):
    asks = [int(i) for i in group.session.config["seller_asks"].split(",")]
    for j in range(1, 6):
        setattr(group, "seller_{}_ask".format(j), asks[j-1])
    bids = [int(i) for i in group.session.config["players_max_bids"].split(",")]
    bids_randomized = random.sample(bids, k=len(bids))
    for i, p in enumerate(group.get_players()):
        p.bid_value = bids_randomized[i]
    
def get_active_players_market(player):
    bids = [(player.id_in_group, player.bid_value)]
    for p in player.get_others_in_group():
        participated = p.field_maybe_none("enter_bid")
        if participated:
            bids.append((p.id_in_group, p.bid_value))
    sorted_bids = sorted(bids, reverse=True, key=lambda x: x[1])
    return sorted_bids

def player_bid(player, entered, section):
    player.enter_bid = int(entered)
    earnings = 0
    player.payoff = 0
    if player.enter_bid:
        asks = sorted([int(i) for i in player.session.config["seller_asks"].split(",")])
        max_ask = max(asks) if player.session.config["treatment_FMI"] else 7
        bids = get_active_players_market(player)
        table_results = [bid + (asks[i], bid[1] >= asks[i]) for i, bid in enumerate(bids)]
        price = table_results[-1][2] if table_results[-1][2] <= max_ask else max_ask
        for p_id, p_bid, s_ask, traded in table_results:
            if p_id == player.id_in_group:
                if traded and s_ask <= price:
                    accepted = "Si"
                    earnings = p_bid - price
                    if section == player.session.winner_section and player.round_number == player.session.winner_round:
                        player.payoff = p_bid - price 
                else:
                    accepted = "No"
                break
    else:
        accepted = "No esta participando"
        price = "No esta participando"

    return {
        "accepted": accepted,
        "price": price,
        "earnings": earnings
    }

def creating_session(subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
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
