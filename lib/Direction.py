from enum import Enum


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    HALT = 4  # TODO: Delete this, should have a pause or stop as a different var. Once player goes, will be facing dir


class AIDirectionChoice(Enum):
    LEFT = 0
    FORWARD = 1
    RIGHT = 2
