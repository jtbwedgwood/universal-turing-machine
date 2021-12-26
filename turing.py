import time

class TuringMachine():

    def __init__(
        self,

        # instructions inputs (state, symbol) outputs (symbol, dir 'L' or 'R', state)
        instructions,
        blank_symbol=None,
        example_state=None,
        example_tape='',
        example_pos=0
    ):

        # Compile instructions if list is passed in
        if isinstance(instructions, list):
            self.instructions = self._compile_dict(instructions)
        else:
            self.instructions = instructions

        # Get states and symbols from instructions
        self.states = set(
            [k[0] for k in self.instructions.keys()]
        )
        self.symbols = set(
            [k[1] for k in self.instructions.keys()]
        )

        # Defaults for init_state and blank_symbol
        if example_state is not None:
            self.example_state = example_state
        else:
            self.example_state = self.states[0]
        if blank_symbol is not None:
            self.blank_symbol = blank_symbol
        else:
            self.blank_symbol = self.symbols[0]
        self.example_tape = example_tape
        self.example_pos = example_pos

    # Function from instructions
    def func(
        self,
        state,
        symbol
    ):
        if (state, symbol) in self.instructions.keys():
            return self.instructions[(state, symbol)]
        return None, None, None

    # Run TM
    def run(
        self,
        tape=None,
        state=None,
        pos=None,
        pause=0
    ):
        if tape is None:
            tape = self.example_tape
        if state is None:
            state = self.example_state
        if pos is None:
            pos = self.example_pos

        # Convert tape to list
        if isinstance(tape, str):
            tape = list(tape)
        while True:
            time.sleep(pause)
            print(state, ''.join(tape[:pos]) + '[' + tape[pos] + ']' + ''.join(tape[pos + 1:]))
            sym, dir, state = self.func(state, tape[pos])
            if state is None:
                return
            tape[pos] = sym
            if dir == 'L':
                pos -= 1
            elif dir == 'R':
                pos += 1
            if pos < 0:
                pos = 0
                tape = [self.blank_symbol] + tape
            elif pos >= len(tape):
                tape.append(self.blank_symbol)

    def _compile_dict(self, l):
        d = {}
        for s in l:
            if len(s) == 5:
                d[(f'{s[0]}', s[1])] = (s[2], s[3], f'{s[4]}')
        return d



if __name__ == '__main__':
    adder.run(pause=1)
