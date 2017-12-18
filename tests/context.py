import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shorty.urlminifier import UrlMinifier
from shorty.strategy.persisted_key import PersistedKey
from shorty.db.memory import Memory
