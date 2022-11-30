# NHS Number Generator

[![Coverage Status](https://coveralls.io/repos/github/Iain-S/nhs_number_generator/badge.svg?branch=master)](https://coveralls.io/github/Iain-S/nhs_number_generator?branch=master)
[![Build Status](https://travis-ci.org/Iain-S/nhs_number_generator.svg?branch=master)](https://travis-ci.org/Iain-S/nhs_number_generator)

Generate and validate NHS numbers in Python 2.7+ and 3.6+.

## To use as a script

Generate five (-n 5) sequential (-d) formatted (-f) nhs numbers:

```
$ python -m nhs_number_generator.generate_nhs_numbers -n 5 -d -f
400 000 0004
400 000 0012
400 000 0020
400 000 0039
400 000 0047
```

Use the -h flag for help:

```
$ python -m nhs_number_generator.generate_nhs_numbers -h
usage: generate_nhs_numbers.py [-h] [-n N] [-d] [-f]

Generate 10-digit NHS numbers.

optional arguments:
  -h, --help           show this help message and exit
  -n N                 the amount to generate
  -d, --deterministic  generate predictably, starting at 4000000004
  -f, --format         format using spaces e.g. 565 228 3297
  ```

## To use as a library

```python
from nhs_number_generator import generate_nhs_numbers

for nhs_number in generate_nhs_numbers.random_nhs_number_generator([(489000000, 489999999)]):
    print(nhs_number)
```
