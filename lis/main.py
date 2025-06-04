#!/usr/bin/env python3

def characterOccurencesIn(string):

    if type(string) is not str:
        raise 'Type needs to be string'
    if not string:
        raise 'String cannot be None'

    occurences = {
        character : string.count(character)
        for character in set(string)
    }

    return occurences

print(characterOccurencesIn("Micaelle"))
