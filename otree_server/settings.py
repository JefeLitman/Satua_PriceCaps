"""File containing the general settings for the oTree app
Version: 1.6
Made By: Edgar RP
"""
from os import environ

SESSION_CONFIGS = [
    dict(
        name='Codigo_Participante',
        app_sequence=['welcome'],
        num_demo_participants=1,
    ),
    dict(
        name='Market_First',
        app_sequence=[
            'informacion', 
            'market_1', 
            'market_2',
            'market_3', 
            'market_4',
            'lottery',
            'assignation',
            "gracias"
        ],
        num_demo_participants=8,
        groups_folder="NA",
        treatment_FME=True,
        treatment_FMI=False,
        treatment_PCE=False,
        seed = 8128,
        max_price = 7,
        seller_asks = "2,2,8,9",
        players_bids = "11,11,12,12"
    ),
    dict(
        name='Lottery_First',
        app_sequence=[
            'informacion', 
            'lottery',
            'assignation',
            'market_1', 
            'market_2',
            'market_3', 
            'market_4',
            "gracias"
        ],
        num_demo_participants=8,
        groups_folder="NA",
        treatment_FME=True,
        treatment_FMI=False,
        treatment_PCE=False,
        seed = 8128,
        max_price = 7,
        seller_asks = "2,2,8,9",
        players_bids = "11,11,12,12"
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=12000, participation_fee=20000, doc=""
)

PARTICIPANT_FIELDS = [
    "consentimiento", 
    "section_setting",
    "chosen_player"
]
SESSION_FIELDS = [
    "winner_section",
    "winner_round",
    "lottery_section_number",
    "assignation_section_number",
    "market_initial_number"
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True

ROOMS = [
    dict(
        name='espera',
        display_name='Sala de espera',
        participant_label_file='labels.txt',
        use_secure_urls=False
    )
]

ADMIN_USERNAME = 'rosario'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7623296763150'
