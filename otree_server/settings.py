"""File containing the general settings for the oTree app
Version: 0.8
Made By: Edgar RP
"""
from os import environ

SESSION_CONFIGS = [
    dict(
        name='Precios_Maximos_Full',
        app_sequence=['consentimiento', 'informacion', 'seccion_1'],
        num_demo_participants=4,
        treatment_FMI=True,
        time_per_practice_period=60,
        time_per_trading_period=20,
        seed = 8128,
        min_ask = 4,
        max_ask = 10,
        min_value = 5,
        max_value = 11,
        increase_ask_by = 1,
        decrease_ask_by = 1,
    ),
    dict(
        name='Precios_Maximos_Simple',
        app_sequence=['consentimiento', 'informacion', 'seccion_1'],
        num_demo_participants=4,
        treatment_FMI=True,
        time_per_practice_period=30,
        time_per_trading_period=20,
        seed = 8128,
        seller_asks = "2,2,8,9,9",
        players_max_bids = "11,11,12,12"
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=15000, doc=""
)

PARTICIPANT_FIELDS = [
    "consentimiento", 
    "winner_section",
    "winner_round"
]
SESSION_FIELDS = []

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
