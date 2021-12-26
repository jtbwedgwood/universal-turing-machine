# Universal Turing Machines

This repository contains some files related to simulating a universal Turing machine. This project was inspired by [this paper](https://arxiv.org/pdf/1904.09828.pdf). The UTM implemented is Rogozhin's (2, 18) from [this paper](https://www.sciencedirect.com/science/article/pii/S0304397596000771). All the details of how the construction works are explained there. For additional details on the mapping between arbitrary Turing machines and tag systems, see section 14.6 of Marvin Minsky's *Computation: Finite and Infinite Machines*, with additional context in chapters 10 and 11.

## Files in this repository

`binary.py` defines a function to convert any Turing machine into one with only two symbols. (In general there will be many more states after the conversion, but I proved that the number of states is O(QS), where Q is the number of states and S the number of symbols of the original TM.) It also defines a class which implements the q, s, m, n representation of a TM discussed in chapter 10 of Minsky.

`machines.py` defines three example Turing machines: a binary adder, the three-state busy beaver, and Rogozhin's (2, 18) UTM.

`tag.py` defines a class representing a tag system and a function for converting a TM into a tag system, again per Minsky.

`turing.py` implements the basic Turing machine class.

`utm.py` defines a function for converting a tag system and a "word" on which the tag system runs into code for the (2, 18) UTM. Since tag systems and Turing machines are isomorphic, this basically is how you write "code" for the UTM.
