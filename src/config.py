# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
import json
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

ADMIN = frozenset(["admin"])
IP_ADDRESS = '0.0.0.0'
PORT=5000
SECRET_KEY = 'rF&UM39t6Rn2S6422776H9e3!*5D62*K'



CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Programming by Reading"
