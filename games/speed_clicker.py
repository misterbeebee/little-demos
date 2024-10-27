import time


def main():

  achnames = [
    'Standerd', 'Quick', 'Super', 'Incredible', 'Patient', 'Endurent', 'Mile',
    'Nonhuman'
  ]
  for i in range(8):
    achnames[i] += ' typer'
  achowned = [False] * 8
  decimals = 2
  while True:
    print('how long in seconds?')
    fail = True
    while fail:
      try:
        typetime = input()
        if typetime == 'settings':
          for i in range(8):
            if achowned[i]:
              print(achnames[i] + ': Owned')
            else:
              print(achnames[i] + ': Unowned')
          while fail:
            try:
              print('decimals?')
              decimals = int(input())
              assert (decimals > 0)
              fail = False
            except:
              print('Error')
          sett = True
        else:
          sett = False
        fail = True
        typetime = float(typetime)
        assert (typetime > 0)
        fail = False
      except:
        if not sett:
          print('Error')
    prev = time.time()
    score = 0
    while time.time() - prev < typetime:
      typed = input()
      if typed != '':
        score += 1
    if typed == '':
      print(
        f'{score} character(s)! ({round(score/typetime,decimals)} per second)')
    else:
      print(
        f'{score-1} character(s)! ({round((score-1)/typetime,decimals)} per second)'
      )
    achievments = [
      score / typetime > 3, score / typetime > 5, score / typetime > 10,
      score / typetime > 15
    ]
    for i in range(4):
      if achievments[i] and not achowned[i]:
        print(['Standerd', 'Quick', 'Super', 'Incredible'][i] +
              ' typer earned!')
        achowned[i] = True
      if typetime >= 10 and achievments[i] and not achowned[i + 4]:
        print(['Patient', 'Endurent', 'Mile', 'Nonhuman'][i] +
              ' typer earned!')
        achowned[i + 4] = True
