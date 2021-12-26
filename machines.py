from turing import TuringMachine

# Example Turing Machines
busy_beaver = TuringMachine(
    ['A01RB', 'A11LC', 'B01LA', 'B11RB', 'C01LB'],
    blank_symbol='0',
    example_state='A',
    example_tape='0',
    example_pos=0
)
adder = TuringMachine(
    ['000R0','011R0', '0__R1', '100R1', '111R1', '1__L2', '201L2', '210L3', '2__R5',
    '300L3', '311L3', '3__L4', '401R0', '410L4', '4_1R0', '51_R5'],
    blank_symbol='_',
    example_state='0',
    example_tape='1_1',
    example_pos=0
)
utm = TuringMachine(
    ['1BRL1', '1CDR1', '1ARL1', '1EBR1', '1DEL1', '1FGR1', '1HIR1', '1GFL1', '1JFR1',
    '1IJL1', '1KLL2', '1LJL2', '1MCL2', '1ONR1', '1NQL1', '1QPR2', '1RAR1',
    '2BAR2', '2CAR2', '2ACL2', '2EDR2', '2DBL2', '2FKR1', '2HGR2', '2GHL2', '2JIR2',
    '2IHL2', '2KFR1', '2LIR2', '2MNR2', '2ONR2', '2NOL2', '2QRR2', '2PRL1', '2RML2'],
    blank_symbol='A',
    example_state='1',
    example_tape='PPFFBFFBBBBBBBBFBBFBBBBBFFBBBBBMBMBM',
    example_pos=25
)
