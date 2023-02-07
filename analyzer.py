from user import User
import pandas as pd
import numpy as np
import sqlalchemy


class Analzyer:
    def __init__(self, user: User):
        self.__user = user