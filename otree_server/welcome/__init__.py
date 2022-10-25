"""File containing the welcome config for the players
Version: 1.1
Made By: Edgar RP
"""
import os
import pandas as pd
from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'welcome'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

def creating_session(subsession):
    labels_path = "./labels.txt"
    participants_file = "./participants_data/google_form.csv"
    history_participants = "./participants_data/history.csv"
    if os.path.isfile(participants_file):
        ids = pd.read_csv(participants_file).values[:,1]
        with open(labels_path, "w") as labels:
            labels.write("\n".join([str(i).upper() for i in ids]))
    else:
        raise AssertionError("There must be the google Form data as csv in participants_data folder")
    if not os.path.isfile(history_participants):
        raise AssertionError("There must be the history of participants data as csv in participants_data folder")
    if os.path.isdir(os.path.join("./participants_data/", subsession.session.code)):
        raise AssertionError("There is a repeated session code in participant_data, try to recreate again the session")

# PAGES
class O001_codigo(Page):
    @staticmethod
    def live_method(player, data):
        base_path = "./participants_data/"
        google_data = pd.read_csv(os.path.join(base_path, "google_form.csv"))
        old_columns = google_data.columns.values
        old_columns[1] = "id"
        google_data.columns = old_columns
        google_data["id"] = [str(i).lower() for i in google_data["id"].values]

        exp_folder = os.path.join(base_path, player.session.code)
        if not os.path.isdir(exp_folder):
            os.mkdir(exp_folder)

        participants_file = os.path.join(exp_folder, "actual_participants.csv")
        if not os.path.isfile(participants_file):
            present_persons = []
            with open(participants_file, "w") as csv:
                csv.write("id,"+",".join(["{}".format(i) for i in range(1, google_data.shape[1]-1)])+"\n")
        else:
            present_persons = pd.read_csv(participants_file).values[:,0]
        
        history = pd.read_csv(os.path.join(base_path, "history.csv"))
        search = google_data.loc[google_data["id"] == str(data).lower()].values
        has_participated = history.loc[history["participant_id"] == str(data).upper()].shape[0] > 0
        if search.shape[0] == 1 and str(data).lower() not in present_persons and not has_participated:
            with open(participants_file, "a") as csv:
                csv.write(",".join(["{}".format(i) for i in search[0,1:]])+"\n")
            return {player.id_in_group: 1}
        else:
            return {player.id_in_group: 0}

page_sequence = [O001_codigo]
