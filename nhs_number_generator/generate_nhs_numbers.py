"""Generate 10-digit NHS numbers with optional formatting.

This module allows you to generate 10-digit NHS numbers, which are the unique patient identifier used by the National
Health Service.  Note that, at some point point in the past, NHS numbers were 9-digits long.

Examples:
    The file can be called from the command line, in which case it prints the numbers directly to the screen:
        $ python generate_nhs_numbers.py

    Alternatively, you can use one of the two types of generator function:
    This one will start at '4000000004' and count up, skipping any invalid numbers or numbers not routinely issued
        >>> deterministic_gen = deterministic_nhs_number_generator()
        >>> next(deterministic_gen)

    This one is (pseudo)random and will generate NHS numbers in the range specified
        >>> random_gen = random_nhs_number_generator([(489000000, 489999999)])
        >>> next(random_gen)

"""

from __future__ import unicode_literals

from argparse import ArgumentParser
from random import choice, randint

check_digit_weights = {0: 10, 1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2}


def calculate_check_digit(nhs_number):
    """Given the first 9 or 10 digits of a 10-digit NHS number, calculates what the check digit should be.

    Returns:
        int: The check digit.  Note that this function may return 10, in which case the NHS number is invalid.

    """

    # The procedure for calculating the check digit, according to:
    # https://www.datadictionary.nhs.uk/data_dictionary/attributes/n/nhs/nhs_number_de.asp

    # Step 1) Multiply each of the first nine digits by a weighting factor
    products = [int(nhs_number[i]) * check_digit_weights[i] for i in range(9)]

    # Step 2) Add the results of each multiplication together.
    sum_products = sum(products)

    # Step 3) Divide the total by 11 and establish the remainder.
    remainder = sum_products % 11

    # Step 4) Subtract the remainder from 11 to give the check digit.
    eleven_minus_remainder = 11 - remainder

    # If the result is 11 then a check digit of 0 is used. If the result is 10 then the NHS number is invalid.
    if eleven_minus_remainder == 11:
        return 0
    else:
        return eleven_minus_remainder


def deterministic_nhs_number_generator(
    ranges=[(400000000, 499999999), (600000000, 708800001)]
):
    """Returns a generator for a predictable sequence of 10-digit NHS numbers.

    The default ranges are the ones currently issued in England, Wales and the Isle of Man.  Numbers outside of this
    range may be valid but could conflict with identifiers used in Northern Ireland and Scotland.
    See https://en.wikipedia.org/wiki/NHS_number

        Args:
        ranges [(int, int), ...]: Specify the ranges for the sequence.  You must exclude the check digits.

    """
    for _range in ranges:
        if _range[1] < _range[0]:
            raise ValueError(
                "The high end of the range should not be lower than the low end."
            )

        if (_range[1] - _range[0]) == 0:
            only_possible_check_digit = calculate_check_digit(
                "{:09d}".format(_range[0])
            )
            if only_possible_check_digit == 10:
                raise ValueError("{:09d} is not a valid NHS number.".format(_range[0]))

    for _range in ranges:
        i = _range[0]

        while i <= _range[1]:
            candidate_number = "{:09d}".format(i)

            check_digit = calculate_check_digit(candidate_number)

            if check_digit != 10:
                yield candidate_number + str(check_digit)

            i += 1

    return


def random_nhs_number_generator(
    ranges=[(400000000, 499999999), (600000000, 708800001)]
):
    """Returns a generator for an unpredictable sequence of 10-digit NHS numbers.

    The default ranges are the ones currently issued in England, Wales and the Isle of Man.  Numbers outside of this
    range may be valid but could conflict with identifiers used in Northern Ireland and Scotland.
    See https://en.wikipedia.org/wiki/NHS_number

        Args:
        ranges [(int, int), ...]: Specify the ranges for the sequence.  You must exclude the check digits.

    """
    for _range in ranges:
        if _range[1] < _range[0]:
            raise ValueError(
                "The high end of the range should not be lower than the low end."
            )

        if (_range[1] - _range[0]) == 0:
            only_possible_check_digit = calculate_check_digit(
                "{:09d}".format(_range[0])
            )
            if only_possible_check_digit == 10:
                raise ValueError("{:09d} is not a valid NHS number.".format(_range[0]))

    while True:
        # Pick a tuple (a, b) at random from ranges and get a random int >= a and <= b.
        # Note that this weights the ranges equally, no matter their size
        candidate_number = "{:09d}".format(randint(*choice(ranges)))
        check_digit = calculate_check_digit(candidate_number)

        if check_digit != 10:
            yield candidate_number + str(check_digit)


def add_separators(nhs_number, separator=" "):
    """Returns the NHS number in 3-3-4 format with a separator in between (a space by default)."""
    return nhs_number[0:3] + separator + nhs_number[3:6] + separator + nhs_number[6:10]


def remove_separators(nhs_number):
    """Remove separators, if there are any, to go from e.g. 123-456-7890 to 1234567890."""
    if not nhs_number[3].isnumeric() and not nhs_number[7].isnumeric():
        return nhs_number[0:3] + nhs_number[4:7] + nhs_number[8:]
    else:
        return nhs_number


def is_valid_nhs_number(nhs_number):
    """Checks whether the NHS number is valid.

    NHS numbers in 3-3-4 format should be converted first, i.e. with remove_separators().

    """
    if (
        (type(nhs_number) != str and type(nhs_number) != type(""))
        or len(nhs_number) != 10
        or not nhs_number.isnumeric()
    ):
        return False

    check_digit = calculate_check_digit(nhs_number)

    # The check digit shouldn't be 10 (how could it be, it is only one digit)
    if check_digit == 10:
        return False

    if str(check_digit) == nhs_number[9]:
        return True
    else:
        return False


def main():
    """Generate 10-digit NHS numbers from the command line."""

    # Define our command line options with sensible defaults and help messages
    parser = ArgumentParser(description="Generate 10-digit NHS numbers.")
    parser.add_argument(
        "-n", required=False, type=int, help="the amount to generate", default=10
    )
    parser.add_argument(
        "-d",
        "--deterministic",
        action="store_const",
        const=True,
        default=False,
        help="whether to generate predictably, starting at 4000000004",
    )
    parser.add_argument(
        "-f",
        "--format",
        action="store_const",
        const=True,
        default=False,
        help="whether to format using spaces e.g. 565 228 3297",
    )

    arguments = parser.parse_args()

    if arguments.deterministic:
        generator = deterministic_nhs_number_generator()
    else:
        generator = random_nhs_number_generator()

    if arguments.format:
        formatter = add_separators
    else:
        formatter = lambda x: x

    for i in range(arguments.n):
        print(formatter(next(generator)))


if __name__ == "__main__":
    main()  # pragma: no cover
