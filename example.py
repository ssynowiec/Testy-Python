from pytest import approx
import random
import pytest
import tempfile
import os


def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
    assert add('space', 'ship') == 'spaceship'
    assert add(0.1, 0.2) == approx(0.3)


def factorial(n):
    """
    Computes the factorial of n.
    """
    if n < 0:
        raise ValueError('received negative input')
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2


def count_word_occurrence_in_string(text, word):
    """
    Counts how often word appears in text.
    Example: if text is "one two one two three four"
             and word is "one", then this function returns 2
    """
    words = text.split()
    return words.count(word)

#
# def test_count_word_occurrence_in_string():
#     assert count_word_occurrence_in_string('AAA BBB', 'AAA') == 1
#     assert count_word_occurrence_in_string('AAA AAA', 'AAA') == 2
#     # What does this last test tell us?
#     assert count_word_occurrence_in_string('AAAAA', 'AAA') == 1


def count_word_occurrence_in_file(file_name, word):
    """
    Counts how often word appears in file file_name.
    Example: if file contains "one two one two three four"
             and word is "one", then this function returns 2
    """
    count = 0
    with open(file_name, 'r') as f:
        for line in f:
            words = line.split()
            count += words.count(word)
    return count


def test_count_word_occurrence_in_file():
    _, temporary_file_name = tempfile.mkstemp()
    with open(temporary_file_name, 'w') as f:
        f.write("one two one two three four")
    count = count_word_occurrence_in_file(temporary_file_name, "one")
    assert count == 2
    os.remove(temporary_file_name)


class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 0

    def go_for_a_walk(self):  # <-- how would you test this function?
        self.hunger += 1


def test_pet():
    p = Pet('asdf')
    assert p.hunger == 0
    p.go_for_a_walk()
    assert p.hunger == 1

    p.hunger = -1
    p.go_for_a_walk()
    assert p.hunger == 0


def fizzbuzz(number):
    if not isinstance(number, int):
        raise TypeError
    if number < 1:
        raise ValueError
    elif number % 15 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return number

def test_fizzbuzz():
    expected_result = [1, 2, "Fizz", 4, "Buzz", "Fizz",
                       7, 8, "Fizz", "Buzz", 11, "Fizz",
                       13, 14, "FizzBuzz", 16, 17, "Fizz", 19, "Buzz"]
    obtained_result = [fizzbuzz(i) for i in range(1, 21)]

    assert obtained_result == expected_result

    with pytest.raises(ValueError):
        fizzbuzz(-5)
    with pytest.raises(ValueError):
        fizzbuzz(0)

    with pytest.raises(TypeError):
        fizzbuzz(1.5)
    with pytest.raises(TypeError):
        fizzbuzz("rabbit")

def main():
    for i in range(1, 100):
        print(fizzbuzz(i))

from collections import Counter


def roll_dice(num_dice):
    return [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(num_dice)]


def yahtzee():
    """
    Play yahtzee with 5 6-sided dice and 3 throws.
    Collect as many of the same dice side as possible.
    Returns the number of same sides.
    """

    # first throw
    result = roll_dice(5)
    most_common_side, how_often = Counter(result).most_common(1)[0]

    # we keep the most common side
    target_side = most_common_side
    num_same_sides = how_often
    if num_same_sides == 5:
        return 5

    # second and third throw
    for _ in [2, 3]:
        throw = roll_dice(5 - num_same_sides)
        num_same_sides += Counter(throw)[target_side]
        if num_same_sides == 5:
            return 5

    return num_same_sides


if __name__ == "__main__":
    num_games = 100

    winning_games = list(
        filter(
            lambda x: x == 5,
            [yahtzee() for _ in range(num_games)],
        )
    )

    print(f"out of the {num_games} games, {len(winning_games)} got a yahtzee!")

def test_roll_dice():
    random.seed(0)
    assert roll_dice(5) == [4, 4, 1, 3, 5]
    assert roll_dice(5) == [4, 4, 3, 4, 3]
    assert roll_dice(5) == [5, 2, 5, 2, 3]


def test_yahtzee():
    random.seed(1)
    num_games = 10000

    winning_games = list(
        filter(
            lambda x: x == 5,
            [yahtzee() for _ in range(num_games)],
        )
    )

    assert len(winning_games) == 460
