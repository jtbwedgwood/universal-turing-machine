from binary import convert_to_binary
from machines import *
from tag import TagSystem, convert_to_tag
from turing import TuringMachine


# Takes a tag system and a tape and generates a UTM tape and starting position
def generate_utm_tape(ts, tape):

    # Need to get a list where halting symbol is last
    symbols = [
        k for k in ts.productions.keys() if ts.productions[k] is not None
    ] + [
        k for k in ts.productions.keys() if ts.productions[k] is None
    ]

    # Generate associated number for each symbol
    N = 1
    numbers = {}
    for sym in symbols:
        numbers[sym] = N
        if ts.productions[sym] is None:
            break
        m = len(ts.productions[sym])
        N += m + 1

    # Make first half of tape
    first_half = ['P', 'P']
    for sym in symbols[:-1][::-1]:
        first_half += ['F', 'F']
        for i, prod_sym in enumerate(ts.productions[sym][::-1]):
            first_half += ['B'] * numbers[prod_sym]
            if i < len(ts.productions[sym]) - 1:
                first_half += ['B', 'F']
    first_half += ['F', 'F']

    # Make second half of tape
    second_half = []
    for sym in tape:
        second_half += ['B'] * numbers[sym] + ['M']
    return ''.join(first_half + second_half), len(first_half) - 1


if __name__ == '__main__':
    ts = convert_to_tag(convert_to_binary(adder))
    print(generate_utm_tape(ts, ts.example_tape))
