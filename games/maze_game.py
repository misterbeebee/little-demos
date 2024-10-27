import random


def main():
  mazelength = 5
  columns = 4
  gems = 5
  spots = list(range(columns * mazelength))
  #for i in range(5):
  #  spots[i]=[]

  #for i in range(columns):
  #    print(3-len(spots[i]))
  #    print(spots)
  #    for j in range(3-len(spots[i])):
  #      door=random.randint(i+1,columns)
  #      while door in spots[i] or i in spots[door]:
  #        door=random.randint(i+1,columns)
  #      spots[i]+=[door]
  #      spots[door]+=[i]
  extracode = '''for i in range(columns):
    while len(spots[i])<3:
      add=random.randint(0,columns)
      while add==i or (add in spots[i]) or (len(spots[add])>=3):
        add=random.randint(0,columns)
      spots[i]+=[add]
      spots[add]+=[i]
    print(spots)'''
  random.shuffle(spots)
  groups = []
  for i in range(columns):
    groups += [spots[(i) * mazelength:(i + 1) * mazelength]]
  maze = list(range(columns * mazelength))
  for i in range(mazelength):
    for j in range(columns):
      if j == 3:
        groups += [spots[0:mazelength]]
      maze[groups[j][i - 1]] = sorted([(groups[j][i - 2]), (groups[j][i]),
                                       (groups[j - 1][i - 1]),
                                       (groups[j + 1][i - 1])])
    groups = groups[:columns]
  pos = 0
  gempos = [0]
  while 0 in gempos:
    random.shuffle(spots)
    gempos = spots[0:gems]
  visited = []
  print('|s represent visited rooms.\n')
  while gems != 0:
    visited += [pos]
    print('You are in room ' + str(pos) + ' and can go to rooms ', end='')
    for i in maze[pos][:-1]:
      if i in visited:
        print('|' + str(i) + '|, ', end='')
      else:
        print(str(i) + ', ', end='')
    if maze[pos][-1] in visited:
      print('and |' + str(maze[pos][-1]) + '|', end='')
    else:
      print('and ' + str(maze[pos][-1]), end='')
    if pos in gempos:
      gempos.pop(gempos.index(pos))
      gems -= 1
    if gems == 1:
      print('. You have 1 gem left to find.')
    else:
      print('. You have ' + str(gems) + ' gems left to find.')
    goto = input()
    while (not goto.isdigit()) or int(goto) not in maze[pos]:
      goto = input()
    pos = int(goto)
  print('YOU WON!')
