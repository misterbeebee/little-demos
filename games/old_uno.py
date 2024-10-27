#!/bin/env python

from typing import List
from terminal_colored_print import colored_sprint
import os
import random
import sys

def clear():
  """Clears the screen.
  
  It uses the Operating System's command to clear the screen."""
  if os.name == 'nt':  # For Windows
    os.system('cls')
  elif os.name == 'posix':  # For Linux/macOS
    os.system('clear')
  else:
    print('\n'*50)


def check_card(played, pile, current_color):
    return (played.color().symbol()=='W'
    or played.rank()==pile.rank()
    or played.color()==pile.color()
    or played.color().symbol()==current_color)


def play_round(discard, hands, turn, current_color):
  current_card=discard[-1]
  if current_color is None:
    print(f'Last played card, to match: {current_card}\n')
  else:
    print(f'Last played card, to match: {current_card} ({current_color})\n')
  current_hand=hands[turn].cardlist()
  for i in range(len(current_hand)):
    print(f'{i+1}: {current_hand[i]}')
  print(f'\nPlayer {turn+1}, which card would you like to play? Type "0" to draw new card.')
  while True:
    choice=input()
    if choice.isdigit():
      choice=int(choice)
      if choice==0: #If player wants to draw
        break
      if 1<=choice<=len(current_hand):
       if check_card(current_hand[choice-1], current_card, current_color):
         break
    print('Bad option. Please choose another card.')
  #print("\n###\nTODO: process selected card\n###\n")
  return choice



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

#f(x) for x in inputlist]


def play_uno():

  FORWARD=1 #Add 1 to turn each time a player goes
  BACKWARD=-1 #Subtract 1 to turn each time a player goes
  COLOR_SYMBOLS=['R', 'Y', 'G', 'B']
  deck = Deck()
  deck.shuffle()

  while True:
    print("How many players? [1 to 10]")
    num_players = input()
    if not num_players.isdigit():
      print("Bad number. Please try again.")
      continue
    num_players = int(num_players)
    if not 1 <= num_players <= 10:
      print("1 to 10 players only.")
      continue
    break

  hands = [Hand() for n in range(num_players)]
  for hand in hands:
    for i in range(7):
      hand.draw(deck)

  turn=0
  direction=FORWARD
  discard=[]
  discard+=[deck.deal()]
  while discard[-1].color().symbol()=='W':
    discard+=[deck.deal()]
  first_card=discard[-1].rank()
  if first_card=='skip':
    turn+=direction #will always be 1
  if first_card=='reverse':
    direction=-direction #Will always be backwards (-1)
  if first_card=='draw 2':
    for i in range(2):
      hands[turn].draw(deck) #Add 2 cards to the hand of the first player
    turn+=direction #Skip the first players turn
  while turn>=num_players:
    turn-=num_players
  while turn<0:
    turn+=num_players
  current_color=None
  game_won=False

  while True:
    clear()
    print(f'Player {turn+1}, it\'s your turn.\nMake sure other players are looking away and press enter.')
    input()

    for i in range(num_players):
      if len(hands[i])==1:
        print(f'Player {i+1} has 1 card.')
      else:         
        print(f'Player {i+1} has {len(hands[i])} cards.')
    result=play_round(discard, hands, turn, current_color) #Chosen card
    if result==0:
      hands[turn].draw(deck)
    else:
      current_color=None #Remove color requirement after a card is played
      played_card=hands[turn].remove(result)
      discard+=[played_card]
      if hands[turn].cardlist()==[]:
        game_won=True
      if played_card.color().symbol()=='W':
        print('Which color would you like to change the pile to? Type the letter.')
        while True:
          current_color=input().upper()
          if current_color in COLOR_SYMBOLS:
            break
          print('Bad option. Please choose another color.')
      if played_card.rank()=='wild draw 4':
        turn+=direction #Skip a turn
        while turn>=num_players:
          turn-=num_players
        while turn<0:
          turn+=num_players
        for i in range(4):
          hands[turn].draw(deck) #Add 4 cards to the hand of the skipped player
      if played_card.rank()=='reverse':
        direction=-direction #Flip the direction
      if played_card.rank()=='skip':
        turn+=direction #It's okay not to fix mod here because we don't need the turn number
        while turn>=num_players:
          turn-=num_players
        while turn<0:
          turn+=num_players
      if played_card.rank()=='draw 2':
        turn+=direction #Skip a turn
        while turn>=num_players:
          turn-=num_players
        while turn<0:
          turn+=num_players
        for i in range(2):
          hands[turn].draw(deck) #Add 2 cards to the hand of the skipped player

    turn+=direction
    while turn>=num_players:
      turn-=num_players
    while turn<0:
      turn+=num_players
    if game_won:
      clear()
      for i in range(num_players):
        if len(hands[i])==1:
          print(f'Player {i+1} has 1 card.')
        else:         
          print(f'Player {i+1} has {len(hands[i])} cards.')
      break


class Card:

  def __init__(self, color, rank):
    self._color = color
    self._rank = rank

  def __str__(self):
    return colored_sprint(text=f"{self._color._symbol} {self._rank}",
                          fg_color=self._color._number,
                          bg_color=None,
                          format=None)

  def color(self):
    return self._color

  def rank(self):
    return self._rank


class Color:

  def __init__(self, symbol, number):
    self._symbol = symbol  #for color blind users
    self._number = number  #To display color

  def __str__(self):
    return colored_sprint(text=f"{self._symbol}",
                          fg_color=self._number,
                          bg_color=None,
                          format=None)

  def symbol(self):
    return self._symbol

  def number(self):
    return self._number


class Stack:
  """Stack of cards, as in a deck or a hand."""

  def __init__(self):
    self._cards = []

  def __str__(self):
    return '\n'.join([str(card) for card in self._cards])

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
    retval=self._cards[idx]
    self._cards=self._cards[:idx]+self._cards[idx+1:]
    return retval


class Deck:
  """Deck of Uno cards."""
  COLORS = [Color('R', 1), Color('G', 28), Color('B', 20), Color('Y', 3)]
  RANKS = ([str(num)
            for num in range(10)] + [str(num) for num in range(1, 10)] +
           ['skip', 'reverse', 'draw 2'] * 2)

  def __init__(self):
    self._cards = Stack()
    self._cards.add(
      [Card(color, rank) for color in Deck.COLORS for rank in Deck.RANKS] +
      [Card(Color('W', 0), 'wild'),
       Card(Color('W', 0), 'wild draw 4')] * 4)

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
    return self._cards.removed(idx-1)


play_uno()

#for c in range(256):
#  print(colored_sprint(text = f"{c}", fg_color = c, bg_color = None, format = None))





####