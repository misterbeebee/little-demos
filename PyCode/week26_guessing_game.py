from random import randint
from time import time


def quantify(n, item, plural=None, padd=None):
  n = str(n)
  if n == '1':
    return '1 ' + item
  if (plural is None) and (padd is None):
    return n + ' ' + item + 's'
  if (plural is None) and (padd is not None):
    return n + ' ' + item + padd
  if (plural is not None) and (padd is None):
    return n + ' ' + plural
  assert ((plural is not None) and (padd is not None),
          'quantify: plural and padd cannot both be specified')


def main():
  MAX = 100
  TIME = 15
  ATTEMPS = 7
  while True:
    tries = ATTEMPS
    guess = 0
    start = time()
    number = randint(1, MAX)
    while guess != number and tries > 0 and time() - start < TIME:
      print(f'You have {quantify(tries, "try", plural="tries")}', end=' ')
      print(f'and {quantify(round(TIME-(time()-start), 1), "second")}')
      guess = 'not a number'
      while not guess.isdigit():
        guess = input(f'Guess a number between 1 and {MAX}\n')
      guess = int(guess)
      if guess > number:
        print('Lower')
        tries -= 1
      if guess < number:
        print('Higher')
        tries -= 1
      if guess == number:
        print('You won!')
      elif tries == 0:
        print(f'You ran out of tries. It was {number}')
        break
      elif time() - start >= TIME:
        print(f'You ran out of time. It was {number}')
        break
    if input('again?\n') not in ['y', 'yes']:
      break