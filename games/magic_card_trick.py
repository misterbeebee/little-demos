import random, sys

from my_lib import clear


def main():
  while True:
    try:
      print("I've written a number on the back of each of these cards.\n")
      print("+--------+     +--------+")
      print("|        |     |        |")
      print("|        |     |        |")
      print("|        |     |        |")
      print("|   A    |     |    B   |")
      print("|        |     |        |")
      print("|        |     |        |")
      print("|        |     |        |")
      print("+--------+     +--------+")

      print("\nThink of a integer between 1 and 1000.")

      print("\nWhat was your number?")

      x = input()
      clear.clear()

      assert ('.' not in x)
      x = int(x)
      assert (0 < x <= 1000)
      print("\nPick a card to flip over, A or B:")

      y = input().upper()
      if (y[0] == 'A'):
        print("\n")
        print("+--------+     +--------+")
        print("|        |     |        |")
        print("|        |     |        |")
        print("|        |     |        |")
        print("|  %4d  |     |  %4d  |" % (x, random.randint(1, 1000)))
        print("|        |     |        |")
        print("|        |     |        |")
        print("|        |     |        |")
        print("+--------+     +--------+")

      elif (y[0] == 'B'):
        print("\n")
        print("+--------+     +--------+")
        print("|        |     |        |")
        print("|        |     |        |")
        print("|        |     |        |")
        print("|  %4d  |     |  %4d  |" % (random.randint(1, 1000), x))
        print("|        |     |        |")
        print("|        |     |        |")
        print("|        |     |        |")
        print("+--------+     +--------+")

      else:
        print("You messed up.")

      print("\nTADA!!\n\n\n")

    except:
      print("\nYou messed up.")
      print("\n")
    print('Go again?')
    if not input().lower().startswith('y'):
      sys.exit()
    clear.clear()


if __name__ == "__main__":
  main()
