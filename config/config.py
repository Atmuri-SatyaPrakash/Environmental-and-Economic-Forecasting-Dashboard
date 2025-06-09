import configparser
import os

# Initialize parser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))

# API Settings
OPENAQ_API_URL = config['API']['openaq_url']
OPENAQ_API_KEY = config['API']['api_key']
# MongoDB Settings
MONGO_URI = config['MongoDB']['uri']
MONGO_DB = config['MongoDB']['database']
MONGO_COLLECTION = config['MongoDB']['collection']

# PostgreSQL Settings
PG_DB = config['PostgreSQL']['dbname']
PG_USER = config['PostgreSQL']['user']
PG_PASSWORD = config['PostgreSQL']['password']
PG_HOST = config['PostgreSQL']['host']

# General Settings
DEBUG = config.getboolean('General', 'debug')

COORDINATES_OPENAQ = config.get('Locations','coordinates')
COORDINATES_GDP = config.get('Locations','country_gdp')
