from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

from flask_caching import Cache

cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

CORS(app, support_credentials=True)

import server.views
