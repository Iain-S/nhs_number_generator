# NHS Number Generator

[![Coverage Status](https://coveralls.io/repos/github/Iain-S/nhs_number_generator/badge.svg)](https://coveralls.io/github/Iain-S/nhs_number_generator)

Generate and validate NHS numbers in Python 2.7+ and 3.6+.

## Installation

```shell
pip install git+https://github.com/Iain-S/nhs_number_generator.git
```

## Usage

### Commandline

Get help with the `-h` flag:

```shell
$ nhs_number_generator -h
usage: nhs_number_generator [-h] [-n N] [-d] [-f]

Generate 10-digit NHS numbers.

options:
  -h, --help           show this help message and exit
  -n N                 the amount to generate
  -d, --deterministic  whether to generate predictably, starting at 4000000004
  -f, --format         whether to format using spaces e.g. 565 228 3297
```

Generate 10, pseudo-random NHS numbers (the default behaviour):

```shell
$ nhs_number_generator
4517270564
6005465694
6640199246
6705661704
4703963035
4391552523
6224020507
4390707728
4421288136
6684220526
```

Generate five (`-n 5`) sequential (`-d`) formatted (`-f`) NHS numbers:

```shell
$ nhs_number_generator -n 5 -d -f
400 000 0004
400 000 0012
400 000 0020
400 000 0039
400 000 0047
```

### Library

Note that both the (pseudo-)random and deterministic generators accept an iterable of ranges.
The beginning and end of each range should be specified as the first nine digits of the NHS numbers,
as the tenth is a check digit and can be calculated from the others.

`random_nhs_number_generator` will return randomly chosen NHS numbers from the ranges supplied.
It will, potentially, run forever and return duplicates, so we need to handle those two things in the calling code:

```python
from nhs_number_generator.generate_nhs_numbers import random_nhs_number_generator

# Generate seven random NHS numbers
numbers = [
    next(random_nhs_number_generator([(489000000, 489999999)])) for _ in range(7)
]

# Keep only one of each
unique_numbers = set(numbers)

print(unique_numbers)
```

`deterministic_nhs_number_generator` will generate all 189,818,183 valid NHS numbers by default.
Alternatively, we can pick only as many numbers as we need or provide a more limited range:

```python
from nhs_number_generator.generate_nhs_numbers import deterministic_nhs_number_generator

# Pick the lowest six valid numbers...
generator = deterministic_nhs_number_generator()
numbers = [next(generator) for _ in range(6)]

print(numbers)

# ...or choose a different set of ranges
print(
    list(
        deterministic_nhs_number_generator(
            [(6000000006, 6000000014), (7000000007, 7000000015)]
        )
    )
)
```
