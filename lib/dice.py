#!/usr/bin/env python
from random import randint


def roll(number, sides, modifier):
    finalroll = 0
    for x in range(number):
        roll = (randint(1, sides))
        finalroll += roll
    return finalroll + modifier


def average(number, sides, modifier):
    avg = 0
    for x in range(1000):
        avg += roll(number, sides, modifier)
    avg /= 1000
    avg = round(avg)
    print(avg)


average(6, 12, 0)

