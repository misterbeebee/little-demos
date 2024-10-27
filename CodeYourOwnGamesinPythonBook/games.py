import random, time, readchar, copy, inspect


def HelloWorld():
  print('Hello world!\nWhat is your name?')
  print(f'It is good to meet you, {input()}')


def GuessTheNumber():
  print('How many guesses do you need?')
  GuessesLeft = '0'
  while not (GuessesLeft.isdigit() and int(GuessesLeft) > 0):
    GuessesLeft = input()
  GuessesLeft = int(GuessesLeft)
  print('What should the largest number be?')
  max = '0'
  while not (max.isdigit() and int(max) > 0):
    max = input()
  max = int(max)
  number = random.randint(1, int(max))
  while GuessesLeft > 0:
    print('Guess')
    Guess = '0'
    while not (Guess.isdigit() and max >= int(Guess) >= 1):
      GuessesLeft -= 1
      Guess = input()
    Guess = int(Guess)
    if number > Guess:
      print('Higher')
    if number < Guess:
      print('Lower')
    if number == Guess:
      if GuessesLeft != 1:
        print(f'Yes!, with {GuessesLeft} guesses to spare')
      else:
        print('Yes!, with 1 guess to spare')
      print('Again? (y/yes to play again)')
      if input().lower() in ['y', 'yes']:
        GuessTheNumber()
      return True
  print(f'The number was {number}')
  print('Again? (y/yes to play again)')
  if input().lower() in ['y', 'yes']:
    GuessTheNumber()
  return False


def Jokes():
  input('What do you get when you cross a snowman with a vampire?')
  print('Frostbite!\n')
  time.sleep(1)
  input('What do dentists call an astronauts cavity?')
  print('A black hole!\n')
  time.sleep(1)
  input('Knock knock')
  input('Who\'s there?')
  print('Interrupting cow (Please type the response)')
  chars = ''
  while len(chars) < 15:
    chars += readchar.readchar()
    print(chars[-1], end='', flush=True)
  print('-MOO\n')
  time.sleep(1)
  print('SLOTH ', end='')
  SlowPrint('Package has left the building', end='')
  input()
  print('SLOTH ', end='')
  SlowPrint('I repeat: Package has left the building... About three hours ago')


def SlowPrint(text, wait=0.1, end='\n'):
  char = 0
  while char < len(text):
    print(text[char], end='', flush=True)
    char += 1
    time.sleep(wait)
  print('', end=end)


def DragonRealm():
  SlowPrint(
    'You are in the land of dragons.\nIn front of you, you see two caves.\nIn one cave, there is a friendly dragon who will share his treasure.\nIn the other cave, a mean one who will eat you on sight...\nWill you enter cave 1 or 2?'
  )
  cave = None
  while not cave in ['1', '2']:
    cave = input()
  SlowPrint(
    'You enter the cave...\nIt is dark and spooky...\nA large dragon sits there and...'
  )
  Messages = ['Gives you treasure!', 'Gobbles you down in one bite!']
  random.shuffle(Messages)
  SlowPrint(Messages[int(cave) - 1] + '\nAgain? (y/yes)')
  if input().lower() in ['y', 'yes']:
    DragonRealm()


def TestMove(board, move, width, blank):
  return (move.isdigit() and 0 < int(move) < width + 1
          and board[0][int(move) - 1] == blank)


def TestWins(board, height, width, player, blank, prints=True):
  for h in range(height):
    for w in range(width):
      for t in [[1, 0], [-1, 0], [1, 1], [0, 1], [1, -1]]:
        try:
          assert ((board[h][w] == board[h + t[1]][w + t[0]] ==
                   board[h + t[1] * 2][w + t[0] * 2] ==
                   board[h + t[1] * 3][w + t[0] * 3] == ['X', 'O'][player])
                  and min(h, w, h + t[1] * 3, w + t[0] * 3) >= 0)

          #print(f'''
          #[{h}][{w}]==
          #[{h+t[1]}][{w+t[0]}]==
          #[{h+t[1]*2}][{w+t[0]*2}]==
          #[{h+t[1]*3}][{w+t[0]*3}]==
          #{['X','O'][player]}''')

          #print(f'''
          #{board[h][w]}==
          #{board[h+t[1]][w+t[0]]}==
          #{board[h+t[1]*2][w+t[0]*2]}==
          #{board[h+t[1]*3][w+t[0]*3]}==
          #{['X','O'][player]}'''
          #)

          for i in range(width):  #Todo: make printBoard()
            if prints: print((i + 1) % 10, end='')
          print()
          for h in range(height):
            for w in range(width):
              if prints: print(board[h][w], end='')
            if prints: print()
          if prints: print(f'player {player+1} wins!')
          return True
        except:
          pass
  if not blank in str(board):
    for i in range(width):  #Todo: make printBoard()
      if prints: print((i + 1) % 10, end='')
    if prints: print()
    for h in range(height):
      for w in range(width):
        if prints: print(board[h][w], end='')
      if prints: print()
    print('Tie!')
    return False


def debuglog(msg):
  """Print caller's method name and line number, to a log file."""
  f = open('debug.text', 'a')
  curframe = inspect.currentframe()
  calframe = inspect.getouterframes(curframe, 2)
  f.write(calframe[1][3] + '\n')
  f.close()


def resetlog():
  """erases log file."""
  f = open('debug.text', 'w')
  f.close()


def getAImove(board, width, blank, height):
  debuglog("getting AI Move")
  testmove = 0
  oldB = copy.deepcopy(board)
  for i in range(7):
    # print(testmove)
    testmove += 1
    while not TestMove(board, str(testmove), width, blank):
      testmove += 1
      if testmove > 7:
        testmove = 0
        while not TestMove(board, str(testmove), width, blank):
          testmove += 1
        return (str(testmove))
    for p in range(2):
      for testheight in range(height):
        board = copy.deepcopy(oldB)
        if board[height - testheight - 1][testmove - 1] == blank:
          board[height - testheight - 1][testmove - 1] = ['X', 'O'][p]
          break
      if TestWins(board, height, width, p, blank, False):
        return str(testmove)
  testmove = 0
  while not TestMove(board, str(testmove), width, blank):
    testmove += 1
  return (str(testmove))


def Connect4(width=7, height=6, blank='_', AI=True):
  player = 0
  board = [[blank for w in range(width)] for h in range(height)]
  while True:
    if not (player == 1 and AI):
      for i in range(width):
        print((i + 1) % 10, end='')
      print()
      for h in range(height):
        for w in range(width):
          print(board[h][w], end='')
        print()
      print(f'Player {player+1}, make your move')
    move = '0'
    while not TestMove(board, move, width, blank):
      if player == 1 and AI:
        move = getAImove(copy.deepcopy(board), width, blank, height)
      else:
        move = input()
    move = int(move)
    for testheight in range(height):
      if board[height - testheight - 1][move - 1] == blank:
        board[height - testheight - 1][move - 1] = ['X', 'O'][player]
        break
    #for h in range(height):
    #  for w in range(width):
    #    for t in [[1,0],[-1,0],[1,1],[0,1],[1,-1]]:
    #      try:
    #        assert((
    #        board[h][w]==
    #        board[h+t[1]][w+t[0]]==
    #        board[h+t[1]*2][w+t[0]*2]==
    #        board[h+t[1]*3][w+t[0]*3]==
    #        ['X','O'][player]) and min(h,w,h+t[1]*3,w+t[0]*3)>=0)

    #print(f'''
    #[{h}][{w}]==
    #[{h+t[1]}][{w+t[0]}]==
    #[{h+t[1]*2}][{w+t[0]*2}]==
    #[{h+t[1]*3}][{w+t[0]*3}]==
    #{['X','O'][player]}''')

    #print(f'''
    #{board[h][w]}==
    #{board[h+t[1]][w+t[0]]}==
    #{board[h+t[1]*2][w+t[0]*2]}==
    #{board[h+t[1]*3][w+t[0]*3]}==
    #{['X','O'][player]}'''
    #)

    #       for i in range(width):  #Todo: make printBoard()
    #         print((i+1)%10,end='')
    #       print()
    #       for h in range(height):
    #         for w in range(width):
    #           print(board[h][w],end='')
    #         print()
    #       print(f'player {player+1} wins!')
    #       return None
    #     except:
    #       pass
    #if not blank in str(board):
    #  for i in range(width):  #Todo: make printBoard()
    #    print((i+1)%10,end='')
    #  print()
    #  for h in range(height):
    #   for w in range(width):
    #    print(board[h][w],end='')
    #   print()
    #  print('Tie!')
    if TestWins(board, height, width, player, blank): return None
    player = (player + 1) % 2


def main():
  game = ''
  print(
    'Programs: 1=Hello world, 2=Guess the number, 3=Jokes, 4=SlowPrint, 5=Dragon Realm, 6=Connect 4'
  )
  game = input()
  if game == '1': HelloWorld()
  if game == '2': GuessTheNumber()
  if game == '3': Jokes()
  if game == '4':
    print('What text?')
    text = input()
    print('Wait time? (Default is 0.1)')
    wait = input()
    if wait.isdigit():
      wait = int(wait)
    else:
      wait = 0.1
    print('End? (Default is newline)')
    end = input()
    SlowPrint(text, wait, end)
  if game == '5': DragonRealm()
  if game == '6':
    print('AI?')
    if input().lower() in ['y', 'yes']:
      Connect4(AI=True)
    else:
      Connect4(AI=False)


resetlog()
while True:
  main()
