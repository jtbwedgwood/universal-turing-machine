import time
from binary import ArithmeticTM, convert_to_binary
from itertools import product
from machines import *
from turing import TuringMachine


SYMBOLS = ['0', '1']
DIRECTIONS = ['L', 'R']


# For testing
busy_beaver = TuringMachine(
    ['A01RB', 'A11LC', 'B01LA', 'B11RB', 'C01LB'],
    blank_symbol='0',
    example_state='A',
    example_tape='0',
    example_pos=0
)


class TagSystem():
    def __init__(
        self,

        # productions takes the form of a dict {symbol: series of symbols to append}
        # Need to specify None for the halting symbol
        productions,
        deletion_number=2,
        example_tape=''
    ):
        self.productions = {
            i: list(productions[i]) if isinstance(productions[i], str) else productions[i]
            for i in productions.keys()
        }
        self.deletion_number = deletion_number
        self.example_tape = example_tape
    def func(
        self,
        tape
    ):
        if isinstance(tape, str):
            tape = list(tape)
        if self.productions[tape[0]] is not None:
            new_tape = tape + self.productions[tape[0]]
            if len(new_tape) > self.deletion_number:
                return new_tape[self.deletion_number:]
        return
    def run(
        self,
        tape=None,
        pause=0,
        verbose=2
    ):
        if tape is None:
            tape = self.example_tape
        if isinstance(tape, str):
            tape = list(tape)
        state = None
        while True:
            time.sleep(pause)
            if verbose == 2:
                print(tape)
            if state != tape[0].split('[')[1].split('(')[0]:
                state = tape[0].split('[')[1].split('(')[0]
            if tape[0].startswith('A['):
                if verbose == 1:
                    print(state, len([s for s in tape if s.startswith('a')]), len([s for s in tape if s.startswith('b')]))
            if self.func(tape) is None:
                return
            tape = self.func(tape)


# Generate a tag system based on a binary Turing machine input
def convert_to_tag(tm):

    # (state, old symbol, new symbol, moves in direction, sees symbol) -> (new state, new symbol, new direction)
    tag_instructions = {
        (k[0], k[1], tm.instructions[k][0], tm.instructions[k][1], i): (
            tm.instructions[k][2],
            tm.instructions[tm.instructions[k][2], i][0],
            tm.instructions[tm.instructions[k][2], i][1]
        )
        for k, i in product(tm.instructions.keys(), SYMBOLS)
        if (tm.instructions[k][2], i) in tm.instructions.keys()
    }

    # Generate productions for tag system
    productions = {}
    for state, old_sym, new_sym, dir in product(tm.states, SYMBOLS, SYMBOLS, DIRECTIONS):

        # String versions of states to append to language characters
        curr_state = f'[{state}({old_sym}{new_sym}{dir})]'
        if (state, old_sym, new_sym, dir, '0') in tag_instructions.keys():
            next_state_0 = f'[{tag_instructions[state, old_sym, new_sym, dir, "0"][0]}(0{tag_instructions[state, old_sym, new_sym, dir, "0"][1]}{tag_instructions[state, old_sym, new_sym, dir, "0"][2]})]'
        else:
            next_state_0 = '[HALT]'
        if (state, old_sym, new_sym, dir, '1') in tag_instructions.keys():
            next_state_1 = f'[{tag_instructions[state, old_sym, new_sym, dir, "1"][0]}(1{tag_instructions[state, old_sym, new_sym, dir, "1"][1]}{tag_instructions[state, old_sym, new_sym, dir, "1"][2]})]'
        else:
            next_state_1 = '[HALT]'

        # General productions
        productions[f'C{curr_state}'] = [f'D1{curr_state}', f'D0{curr_state}']
        productions[f'c{curr_state}'] = [f'd1{curr_state}', f'd0{curr_state}']
        productions[f'S{curr_state}'] = [f'T1{curr_state}', f'T0{curr_state}']
        productions[f's{curr_state}'] = [f't1{curr_state}', f't0{curr_state}']

        # Conditional productions
        if dir == 'R':
            if new_sym == '0':
                productions[f'A{curr_state}'] = [f'C{curr_state}', f'c{curr_state}']
            if new_sym == '1':
                productions[f'A{curr_state}'] = [f'C{curr_state}', f'c{curr_state}', f'c{curr_state}', f'c{curr_state}']
            productions[f'a{curr_state}'] = [f'c{curr_state}', f'c{curr_state}', f'c{curr_state}', f'c{curr_state}']
            productions[f'B{curr_state}'] = [f'S{curr_state}']
            productions[f'b{curr_state}'] = [f's{curr_state}']
            productions[f'D1{curr_state}'] = [f'A{next_state_1}', f'a{next_state_1}']
            productions[f'd1{curr_state}'] = [f'a{next_state_1}', f'a{next_state_1}']
            productions[f'D0{curr_state}'] = [f'a{next_state_0}', f'A{next_state_0}', f'a{next_state_0}']
            productions[f'd0{curr_state}'] = [f'a{next_state_0}', f'a{next_state_0}']
            productions[f'T1{curr_state}'] = [f'B{next_state_1}', f'b{next_state_1}']
            productions[f't1{curr_state}'] = [f'b{next_state_1}', f'b{next_state_1}']
            productions[f'T0{curr_state}'] = [f'B{next_state_0}', f'b{next_state_0}']
            productions[f't0{curr_state}'] = [f'b{next_state_0}', f'b{next_state_0}']
        if dir == 'L':
            productions[f'A{curr_state}'] = [f'A*{curr_state}', f'a*{curr_state}']
            productions[f'a{curr_state}'] = [f'a*{curr_state}', f'a*{curr_state}']
            if new_sym == '0':
                productions[f'B{curr_state}'] = [f'C{curr_state}', f'c{curr_state}']
            if new_sym == '1':
                productions[f'B{curr_state}'] = [f'C{curr_state}', f'c{curr_state}', f'c{curr_state}', f'c{curr_state}']
            productions[f'b{curr_state}'] = [f'c{curr_state}', f'c{curr_state}', f'c{curr_state}', f'c{curr_state}']
            productions[f'D1{curr_state}'] = [f'B*1{curr_state}', f'b*1{curr_state}']
            productions[f'd1{curr_state}'] = [f'b*1{curr_state}', f'b*1{curr_state}']
            productions[f'D0{curr_state}'] = [f'b*0{curr_state}', f'B*0{curr_state}', f'b*0{curr_state}']
            productions[f'd0{curr_state}'] = [f'b*0{curr_state}', f'b*0{curr_state}']
            productions[f'T1{curr_state}'] = [f'A{next_state_1}', f'a{next_state_1}']
            productions[f't1{curr_state}'] = [f'a{next_state_1}', f'a{next_state_1}']
            productions[f'T0{curr_state}'] = [f'A{next_state_0}', f'a{next_state_0}']
            productions[f't0{curr_state}'] = [f'a{next_state_0}', f'a{next_state_0}']
            productions[f'A*{curr_state}'] = [f'S{curr_state}']
            productions[f'a*{curr_state}'] = [f's{curr_state}']
            productions[f'B*0{curr_state}'] = [f'B{next_state_0}', f'b{next_state_0}']
            productions[f'b*0{curr_state}'] = [f'b{next_state_0}', f'b{next_state_0}']
            productions[f'B*1{curr_state}'] = [f'B{next_state_1}', f'b{next_state_1}']
            productions[f'b*1{curr_state}'] = [f'b{next_state_1}', f'b{next_state_1}']

    # We have to define productions for A[HALT], etc, even though they will not be used
    # We arbitrarily assign values of themselves to symbols other than A[HALT]
    productions['A[HALT]'] = None
    productions['a[HALT]'] = ['a[HALT]']
    productions['B[HALT]'] = ['B[HALT]']
    productions['b[HALT]'] = ['b[HALT]']

    # Construct example tape
    atm = ArithmeticTM(tm)
    q, s, m, n = atm.get_qsmn()
    init_state = f'[{q}({tm.example_tape[tm.example_pos]}{tm.instructions[q, tm.example_tape[tm.example_pos]][0]}{tm.instructions[q, tm.example_tape[tm.example_pos]][1]})]'
    tape = [f'A{init_state}', f'a{init_state}'] + m * [f'a{init_state}', f'a{init_state}'] + [f'B{init_state}', f'b{init_state}'] + n * [f'b{init_state}', f'b{init_state}']

    # Generate tag system
    return TagSystem(
        productions,
        example_tape=tape
    )


if __name__ == '__main__':
    binary_adder = convert_to_binary(adder)
    ts = convert_to_tag(binary_adder)
    ts.run(verbose=1)
