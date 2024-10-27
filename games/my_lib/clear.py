import os


def clear():
  """Clears the screen.
  
  It uses the Operating System's command to clear the screen."""
  if os.name == 'nt':  # For Windows
    os.system('cls')
  elif os.name == 'posix':  # For Linux/macOS
    os.system('clear')
  else:
    print('\n'*50)


if __name__ == '__main__':
  clear()
