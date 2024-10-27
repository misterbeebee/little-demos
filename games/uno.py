#!/bin/env python

from typing import Any, List, Literal
from terminal_colored_print import colored_sprint, colored_print
import os
import pywebio
from pywebio.input import FLOAT, TEXT, NUMBER
import random
import sys
from collections.abc import MutableSequence


def listify(obj):
    return obj if isinstance(obj, MutableSequence) else [obj]


class FormattedText:
    def __init__(self, text, fg_color=None, bg_color=None, format=None):
        self._text = text
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._format = format


class UI:
    def __init__(self) -> None:
        pass

    def input(self, type: Literal["text"]):
        raise NotImplementedError()

    def output(self, obj: str | FormattedText):
        raise NotImplementedError()


class ConsoleUI(UI):
    def __init__(self) -> None:
        super().__init__()

    def input(self, type: Literal["text"]):
        match type:
            case pywebio.input.TEXT:
                return input()
            case pywebio.input.NUMBER:
                while True:
                    user_input = input()
                    if user_input.isdigit():
                        return int(user_input)
                    else:
                        print("Bad number. Please try again.")

    def output(self, objs: Any | List[str | FormattedText], sep="", end="\n"):
        objs = listify(objs)
        for obj in objs:
            if isinstance(obj, FormattedText):
                colored_print(
                    obj._text,
                    end="",
                    fg_color=obj._fg_color,
                    bg_color=obj._bg_color,
                    format=obj._format,
                )
            elif isinstance(obj, str):
                print(obj, end="")
            elif isinstance(obj, Color):
                self.output(
                    FormattedText(
                        text=f"{obj._symbol}",
                        fg_color=obj._number,
                        bg_color=None,
                        format=None,
                    )
                )
            elif isinstance(obj, Hand):
                self.output(obj._cards, sep="")
            elif isinstance(obj, Deck):
                self.output(obj.cards())
            elif isinstance(obj, Stack):
                for card in obj.cards():
                    self.output(card)
            elif isinstance(obj, Card):
                self.output(
                    FormattedText(
                        text=f"{obj._color._symbol} {obj._rank}",
                        fg_color=obj._color._number,
                        bg_color=None,
                        format=None,
                    ),
                    sep="\n",
                    end="",
                )
            else:
                raise Exception("Unknown output type: " + type(obj))
            print(sep, end="")

    def clear(self):
        """Clears the screen.

        It uses the Operating System's command to clear the screen."""
        if os.name == "nt":  # For Windows
            os.system("cls")
        elif os.name == "posix":  # For Linux/macOS
            os.system("clear")
        else:
            put_text("\n" * 50)


class WebUI(UI):

    def __init__(self) -> None:
        super().__init__()
        self._main_scope = "scrollable"
        pywebio.output.put_scrollable(
            pywebio.output.put_scope(self._main_scope), height=550, keep_bottom=True
        )

    def input(self, type: Literal["text"]):
        match type:
            case pywebio.input.TEXT | pywebio.input.NUMBER | _:
                return pywebio.input.input(type=type)

    def output(self, objs, end=None, sep=""):
        with pywebio.output.use_scope(self._main_scope):
            objs = listify(objs)
            for obj in objs:
                print(f"{type(obj)}: [{obj}]")
                if isinstance(obj, FormattedText):
                    pywebio.output.style(
                        [
                            pywebio.output.put_text(
                                obj._text, inline=True, scope=self._main_scope
                            ),
                        ],
                        ";".join(
                            [
                                f"color: {obj._fg_color}",
                                f"background-color: {obj._bg_color}",
                                # TODO: obj._format
                            ]
                        ),
                    )

                elif isinstance(obj, str):
                    if obj == "\n":
                        pywebio.output.put_text(
                            "", inline=False, scope=self._main_scope
                        )
                    else:
                        pywebio.output.put_text(
                            obj, inline=True, scope=self._main_scope
                        )
                elif isinstance(obj, Color):
                    pywebio.output.put_text(f"{obj._symbol}", inline=True).style(
                        f"color: {obj._html_name}"
                    )
                elif isinstance(obj, Hand):
                    self.output(obj._cards)
                elif isinstance(obj, Deck):
                    self.output(obj.cards())
                elif isinstance(obj, Stack):
                    for card in obj.cards():
                        self.output(card)
                elif isinstance(obj, Card):
                    pywebio.output.put_text(
                        f"{obj._color.symbol()} {obj._rank}",
                        inline=True,
                        scope=self._main_scope,
                    ).style(
                        ";".join(
                            [
                                f"color: {obj._color._html_name}",
                                # f'background-color: {obj.bg_color}' # not useful yet
                                # TODO: obj.format
                            ]
                        )
                    )
                else:
                    raise Exception("Unknown output type: " + str(type(obj)))
            if end:
                self.output(end)

            pywebio.output.scroll_to(
                position=pywebio.output.Position.BOTTOM, scope=self._main_scope
            )

    def clear(self):
        with pywebio.output.use_scope(self._main_scope):
            pywebio.output.clear()


# Shuffle deck.
# Deal cards.
# Ask Player 1 for move.
# Validate move.
# Check if game over.

# Check whose turn it is.

# Create deck
# Shuffle deck.
# Deal 1 players hand
# Print hand.
# End game.

# f(x) for x in inputlist]


class Game:
    STARTING_HAND_SIZE = 7

    def __init__(self):
        self._ui = WebUI()
        # self._ui = ConsoleUI()

    def check_card(self, played, pile, current_color):
        return (
            played.color().symbol() == "W"
            or played.rank() == pile.rank()
            or played.color() == pile.color()
            or played.color().symbol() == current_color
        )

    def play_round(self, discard, hands, turn, current_color):
        current_card = discard[-1]
        if current_color is None:
            self._ui.output([f"Last played card, to match: ", current_card, "\n"])
        else:
            self._ui.output(
                [
                    f"Last played card, to match: ",
                    current_card,
                    " ",
                    Deck.find_color(current_color),
                    "\n",
                ]
            )
        current_hand = hands[turn].cardlist()
        for i in range(len(current_hand)):
            self._ui.output([f"{i+1}: ", current_hand[i]], end="\n")
        self._ui.output(
            [
                f"\nPlayer {turn+1}, which card would you like to play?\n",
                'Type "0" to draw new card.\n\n',
            ]
        )
        while True:
            choice = self._ui.input(type=pywebio.input.NUMBER)
            if choice == 0:  # If player wants to draw
                break
            if choice is not None and 1 <= choice <= len(current_hand):
                if self.check_card(
                    current_hand[choice - 1], current_card, current_color
                ):
                    break
            self._ui.output("Bad option. Please choose another card.\n")
        return choice

    def play_uno(self):

        FORWARD = 1  # Add 1 to turn each time a player goes
        BACKWARD = -1  # Subtract 1 to turn each time a player goes
        deck = Deck()
        deck.shuffle()

        while True:
            min = 1
            max = 10
            self._ui.output(f"How many players? [{min} to {max}]\n")
            num_players = self._ui.input(type=pywebio.input.NUMBER)
            if not (num_players and min <= num_players <= max):
                self._ui.output(f"{min} to {max} players only.\n")
                continue
            break

        hands = [Hand() for n in range(num_players)]
        for hand in hands:
            for i in range(Game.STARTING_HAND_SIZE):
                hand.draw(deck)

        turn = 0
        direction = FORWARD
        discard = []
        discard += [deck.deal()]
        while discard[-1].color().symbol() == "W":
            discard += [deck.deal()]
        first_card = discard[-1].rank()
        if first_card == "skip":
            turn += direction  # will always be 1
        if first_card == "reverse":
            direction = -direction  # Will always be backwards (-1)
        if first_card == "draw 2":
            for i in range(2):
                hands[turn].draw(deck)  # Add 2 cards to the hand of the first player
            turn += direction  # Skip the first players turn
        while turn >= num_players:
            turn -= num_players
        while turn < 0:
            turn += num_players
        current_color = None
        game_won = False

        while True:
            self._ui.clear()
            self._ui.output(
                [
                    f"Player {turn+1}, it's your turn.\n",
                    "Make sure other players are looking away and press Enter.\n\n",
                ]
            )
            self._ui.input(type=pywebio.input.TEXT)

            for i in range(num_players):
                if len(hands[i]) == 1:
                    self._ui.output([f"Player {i+1} has 1 card.", "\n"])
                else:
                    self._ui.output([f"Player {i+1} has {len(hands[i])} cards.", "\n"])
            result = self.play_round(discard, hands, turn, current_color)  # Chosen card
            if result == 0:
                hands[turn].draw(deck)
            else:
                current_color = None  # Remove color requirement after a card is played
                played_card = hands[turn].remove(result)
                discard += [played_card]
                if hands[turn].cardlist() == []:
                    game_won = True
                if played_card.color().symbol() == "W":
                    self._ui.output(
                        [
                            f"Which color would you like to change the pile to? Type the letter ["
                        ]
                        + Deck.COLORS
                        + ["]\n"],
                        sep="",
                    )
                    while True:
                        current_color = self._ui.input(type=pywebio.input.TEXT).upper()
                        if current_color in Deck.COLOR_SYMBOLS:
                            break
                        self._ui.output("Bad option. Please choose another color.\n")
                if played_card.rank() == "wild draw 4":
                    turn += direction  # Skip a turn
                    while turn >= num_players:
                        turn -= num_players
                    while turn < 0:
                        turn += num_players
                    for i in range(4):
                        hands[turn].draw(
                            deck
                        )  # Add 4 cards to the hand of the skipped player
                if played_card.rank() == "reverse":
                    direction = -direction  # Flip the direction
                if played_card.rank() == "skip":
                    turn += direction  # It's okay not to fix mod here because we don't need the turn number
                    while turn >= num_players:
                        turn -= num_players
                    while turn < 0:
                        turn += num_players
                if played_card.rank() == "draw 2":
                    turn += direction  # Skip a turn
                    while turn >= num_players:
                        turn -= num_players
                    while turn < 0:
                        turn += num_players
                    for i in range(2):
                        hands[turn].draw(
                            deck
                        )  # Add 2 cards to the hand of the skipped player

            turn += direction
            while turn >= num_players:
                turn -= num_players
            while turn < 0:
                turn += num_players
            if game_won:
                self._ui.clear()
                for i in range(num_players):
                    if len(hands[i]) == 1:
                        self._ui.output(f"Player {i+1} has 1 card.\n")
                    else:
                        self._ui.output(f"Player {i+1} has {len(hands[i])} cards.\n")
                break


class Color:

    def __init__(self, symbol, html_name, number):
        self._symbol = symbol  # for color blind users
        self._number = number  # To display color in console
        self._html_name = html_name  # To display color in HTML

    def __str__(self):
        return colored_sprint(
            FormattedText(
                text=f"{self._symbol}",
                fg_color=self._number,
                bg_color=None,
                format=None,
            )
        )

    def symbol(self):
        return self._symbol

    def number(self):
        return self._number


class Card:
    def __init__(self, color: Color, rank):
        self._color = color
        self._rank = rank

    def color(self):
        return self._color

    def rank(self):
        return self._rank


class Stack:
    """Stack of cards, as in a deck or a hand."""

    def __init__(self):
        self._cards = []

    def add(self, cards: List[Card]):
        self._cards = self._cards + (cards if type(cards) == list else [cards])

    def shuffle(self):
        random.shuffle(self._cards)

    def cards(self):
        return self._cards

    def pop(self):
        return self._cards.pop()

    def __len__(self):
        return len(self._cards)

    def removed(self, idx) -> Card:
        retval = self._cards[idx]
        self._cards = self._cards[:idx] + self._cards[idx + 1 :]
        return retval


class Deck:
    """Deck of Uno cards."""

    COLORS = [
        Color("R", "red", 1),
        Color("G", "green", 28),
        Color("B", "blue", 20),
        Color("Y", "orange", 3),
    ]

    def find_color(symbol: str) -> Color:
        for color in Deck.COLORS:
            if symbol == color.symbol():
                return color

    COLOR_SYMBOLS = [color.symbol() for color in COLORS]

    # COLOR_MAP
    RANKS = (
        [str(num) for num in range(10)]
        + [str(num) for num in range(1, 10)]
        + ["skip", "reverse", "draw 2"] * 2
    )

    def __init__(self):
        self._cards = Stack()
        self._cards.add(
            [Card(color, rank) for color in Deck.COLORS for rank in Deck.RANKS]
            + [
                Card(Color("W", "black", 0), "wild"),
                Card(Color("W", "black", 0), "wild draw 4"),
            ]
            * 4
        )

    def __str__(self):
        return str(self._cards)

    def __len__(self):
        return len(self._cards)

    def shuffle(self):
        self._cards.shuffle()

    def deal(self):
        return self._cards.pop()


class Hand:
    """One player's hand of cards for a game."""

    def __init__(self):
        self._cards = Stack()

    def __str__(self):
        return str(self._cards) + "\n"

    def draw(self, deck):
        self._cards.add(deck.deal())

    def cardlist(self):
        return self._cards.cards()

    def __len__(self):
        return len(self._cards)

    def remove(self, idx):
        return self._cards.removed(idx - 1)


Game().play_uno()

# for c in range(256):
#  print(colored_sprint(text = f"{c}", fg_color = c, bg_color = None, format = None))


####
