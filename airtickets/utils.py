import datetime
import re

import requests
import random

from bs4 import BeautifulSoup

from mainapp.models import Flight, Airport, Aircompany, Depature


def find_dict_in_list(list, key):
    r = ''
    try:
        r = next(item for item in list if item["to"] == key)
    except Exception as err:
        pass
    return r


