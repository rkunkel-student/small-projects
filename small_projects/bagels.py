#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""file: bagels.py

Bagels is a deductive logic game, in which the player guesses a secret three digit number.

The game offers one of three hints depending on the player's guess, these include:

* Pico - When your guess has the correct digit in the wrong place.
* Fermi - When your guess has the correct digit in the correct place.
* Bagels - When your guess has no correct digits in the correct places.

The player has 10 guesses to succeed.

"""
import random
import sys
from typing import Final, List, Union

class App:
    """Container for the small project bagels.
    
    Params:
        MAX_GUESSES (Final[int]): Max number of guesses to allow the player to use. Default is 10.
        MAX_DIGITS (Final[int]): Max number of digits for the secret number to contain. Default is 3.
        done (bool): Flag indicating if App has finished processing.

    """
    MAX_GUESSES: Final[int] = 10
    MAX_DIGITS: Final[int] = 3  # Hardlimit of 9
    done: bool = False

    @classmethod
    def get_clues(cls) -> Union[List[str]|List[None]]:
        """Provides a string containing the clues for current guess.
        
        Returns:
            List[str]: List of string containing relevant clues, otherwise returns [].

        """
        clues: List[str] = []
        for index, digit in enumerate(cls.guess):
            if digit == cls.secret_number[index]:
                clues.append("Fermi")
            elif digit in cls.secret_number:
                clues.append("Pico")

        # if no correct digits
        if not clues:
            clues.append("Bagels")

        # else-if all correct digits
        elif clues.count("Fermi") == 3:
            clues.clear()
            print("You got it!")

        # shuffle clues to prevent hint position from giving away information
        elif len(clues) > 1:  # only shuffle if more than one element
            # shuffle(clues)
            # sort is faster than shuffle and obfuscates information just the same
            clues.sort()
        
        return clues

    @classmethod
    def player_input(cls) -> List[int]:
        """Prompts user for a three-digit number.

        Continues current prompt until valid response is received.

        Returns:
            List[int]: A List of three integer elements. Ex: [1, 2, 3]

        """

        done: bool = False
        while not done:
            raw = input("> ")

            try:
                raw = [int(x) for x in raw]
            except ValueError:
                continue

            if len(raw) != 3:
                continue

            done = True

        return raw

    @classmethod
    def play_again(cls) -> bool:
        """Prompts user for play again response.

        Returns:
            bool: True on 'yes' response, otherwise False.

        """
        print("Play again? Answer <Yes/no>: ")
        answer = input("> ").lower()
        if "yes" == answer:
            return True

        return False

    @classmethod
    def run(cls) -> None:
        """Game logic."""
        cls.possible_numbers: List[int] = [x for x in range(1, 10)]
        random.shuffle(cls.possible_numbers)
        cls.secret_number: List[int] = cls.possible_numbers[:3]
        print("I have thought of a number.")

        num_guesses: int = 0
        while num_guesses < cls.MAX_GUESSES:
            num_guesses += 1
            print(f"Guess #{num_guesses}")
            cls.guess = cls.player_input()
            clues = cls.get_clues()

            # if player has won, exit loop
            if not clues:
                return
            
            # otherwise, print clues
            print(" ".join(clues))

            # check if player used all their guesses
            if num_guesses == cls.MAX_GUESSES:
                print("Sorry, that's a game over!")


def main() -> int:
    """Main entrance to the application."""
    print(f"I am thinking of a secret {App.MAX_DIGITS} digit number. No digit will be repeated.")
    print("Here are some clues:")
    print(" 'Pico'   - When your guess has the correct digit in the wrong place.")
    print(" 'Fermi'  - When your guess has the correct digit in the correct place.")
    print(" 'Bagels' - When your guess has no correct digits.")
    print(f"You have {App.MAX_GUESSES} guesses.")

    while not App.done:
        App.run()
        if not App.play_again():
            print("Thanks for playing!")
            App.done = True

    return 0

if __name__ == "__main__":
    sys.exit(main())
