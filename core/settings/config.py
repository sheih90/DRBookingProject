from enum import Enum

import requests
import self

from core.clients.endpoints import Endpoints


class Users(Enum):
    USERNAME : "admin"
    PASSWORD : "password123"

class Timeouts(Enum):
    TIMEOUT = 5

