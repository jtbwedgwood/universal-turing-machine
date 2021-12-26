import math
import time
from itertools import product
from machines import *
from turing import TuringMachine


BLANK = '0'
SYMBOLS = ['0', '1']
DIRECTIONS = ['L', 'R']


def convert_to_binary(tm):
    k = math.ceil(
        math.log(len(tm.symbols), 2)
    )
    symbols = [tm.blank_symbol] + [sym for sym in list(tm.symbols) if sym != tm.blank_symbol]
    symbol_map = {
        sym: BLANK * (k - len(bin(i)) + 2) + bin(i)[2:]
        for i, sym in enumerate(symbols)
    }
    binary_instructions = {
        (k[0], symbol_map[k[1]]): (symbol_map[tm.instructions[k][0]], tm.instructions[k][1], tm.instructions[k][2])
        for k in tm.instructions.keys()
    }

    # Construct list of binary strings of length < k
    binary_strings = ['']
    for i in range(1, k):
        binary_strings += [
            ''.join(bs) for bs in product('01', repeat=i)
        ]

    # Read instructions
    read_instructions = {
        (f'Read_{q}_{s}', i): (i, 'L', f'Read_{q}_{i + s}')
        for q, s, i in product(tm.states, binary_strings, SYMBOLS)
        if len(s) < k - 1
    }

    # Transition from read to write
    read_to_write_instructions = {}
    for q, s, i in product(tm.states, binary_strings, SYMBOLS):
        if len(s) == k - 1 and (q, i + s) in binary_instructions.keys():
            new = binary_instructions[q, i + s]
            read_to_write_instructions[f'Read_{q}_{s}', i] = (
                new[0][0],
                'R',
                f'Write{new[1]}_{new[2]}_{new[0][1:]}'
            )

    # Write instructions
    write_instructions = {}
    for q, s, i, d in product(tm.states, binary_strings, SYMBOLS, DIRECTIONS):
        if len(s) > 1:
            write_instructions[f'Write{d}_{q}_{s}', i] = (s[0], 'R', f'Write{d}_{q}_{s[1:]}')
        if len(s) == 1:
            write_instructions[f'Write{d}_{q}_{s}', i] = (s, 'R', f'Write{d}_{q}_')

    # Transition from write to move
    write_to_move_instructions = {
        (f'Write{d}_{q}_', i): (i, 'L', f'Move{d}_{q}_{k}')
        for q, i, d in product(tm.states, SYMBOLS, DIRECTIONS)
    }

    # Move instructions
    move_instructions = {
        (f'Move{d}_{q}_{n}', i): (i, d, f'Move{d}_{q}_{n - 1}')
        for q, i, d, n in product(tm.states, SYMBOLS, DIRECTIONS, range(1, k + 1))
    }

    # Transition from move to read
    move_to_read_instructions = {
        (f'Move{d}_{q}_1', i): (i, d, f'Read_{q}_')
        for q, i, d in product(tm.states, SYMBOLS, DIRECTIONS)
    }
    return TuringMachine(
        {
            **read_instructions,
            **read_to_write_instructions,
            **write_instructions,
            **write_to_move_instructions,
            **move_instructions,
            **move_to_read_instructions
        },
        blank_symbol=BLANK,
        example_state=f'Read_{tm.example_state}_',
        example_tape=''.join([symbol_map[c] for c in tm.example_tape]),
        example_pos=(tm.example_pos + 1) * k - 1
    )


# (q, s, m, n) representation of a binary Turing Machine
class ArithmeticTM():
    def __init__(
        self,
        tm
    ):
        self.tm = tm
        if set(self.tm.symbols) != {'0', '1'}:
            raise ValueError("Must pass in a binary TM with symbols '0' and '1'")
    def func(self, q, s, m, n):
        if (q, str(s)) not in self.tm.instructions.keys():
            return
        new = self.tm.instructions[q, str(s)]
        return (
            new[2],
            (m % 2) * (new[1] == 'L') + (n % 2) * (new[1] == 'R'),
            (2 * m + int(new[0])) * (new[1] == 'R') + (m // 2) * (new[1] == 'L'),
            (2 * n + int(new[0])) * (new[1] == 'L') + (n // 2) * (new[1] == 'R')
        )
    def run(
        self,
        tape=None,
        state=None,
        pos=None,
        pause=0
    ):

        # Initialize
        q, s, m, n = self.get_qsmn(tape, state, pos)
        while True:
            time.sleep(pause)
            print(q, s, m, n)
            if self.func(q, s, m, n) is None:
                return
            q, s, m, n = self.func(q, s, m, n)
    def get_qsmn(
        self,
        tape=None,
        state=None,
        pos=None
    ):
        if tape is None:
            tape = self.tm.example_tape
        if state is None:
            state = self.tm.example_state
        if pos is None:
            pos = self.tm.example_pos

        # Convert tape to string
        if isinstance(tape, list):
            tape = ''.join(tape)

        # Initialize
        return (
            state,
            int(tape[pos]),
            int(tape[:pos], 2) if pos > 0 else 0,
            int(tape[:pos:-1], 2) if pos < len(tape) - 1 else 0
        )



if __name__ == '__main__':
    tm = convert_to_binary(adder)
    tm.run()
