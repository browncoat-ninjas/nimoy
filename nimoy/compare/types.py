from enum import Enum


class Types(Enum):
    EQUAL = 1
    NOT_EQUAL = 2
    LESS_THAN = 3
    LESS_THAN_EQUAL = 4
    GREATER_THAN = 5
    GREATER_THAN_EQUAL = 6
    IS = 7
    IS_NOT = 8
    IN = 9
    NOT_IN = 10
    MATCHES_REGEXP = 11
