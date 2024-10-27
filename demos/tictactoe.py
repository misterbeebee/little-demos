import random, sys
def Draw_Board(board):
  HLINE=' '+'+---'*8+'+'
  VLINE=' '+'|   '*9+'|'
  print(' 1   2   3   4   5   6   7   8')
  print(HLINE)
  for y in range(8):
    print(VLINE)
    print(y+1,end='')
    for x in range(8):
      print(f'| {board[x][y]} ',end='')
    print(f'|\n{VLINE}\n{HLINE}')
def Reset_Board(b):
  b=[[' ']*8]*8
  b[3][3]='X'
  b[4][4]='X'
  b[3][4]='O'
  b[4][3]='O'
def Get_New_Board():
  board=[]
  for i in range(8):
    board.append([' '*8])
  return board
def Is_Valid_Move(board,tile,xstart,ystart):
  if board[xstart][ystart]!=' 'or not Is_On_Board(xstart,ystart):
    return False
    board[xstart][ystart]=tile
    otherTile=['X','O','X'][['X','O'].index(tile)+1]
    tilesToFlip=[]
    for xdirection,ydirection in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]:
      x,y=xstart,ystart
      x+=xdirection
      y+=ydirection
      if IsOnBoard(x,y) and boa