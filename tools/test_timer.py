#Records test answers and time entered
#Asks for question number and answer, storing it in a variable
#List of answers stings and time
import time
import random

part = 0
global_testing = True
script = [
  '6',  # questions
  '',  # Ready to stary
  '1',
  'A',
  '3',  # skipped question 2 without working on it.
  'C',
  '4',
  '',  # no answer for question 4
  '5',
  'D',
  '3',  # went back to check work,
  'E',  # updated answer
  'stop'
]


def getinput():
  global script
  global global_testing
  if global_testing:
    save = script[0]
    script = script[1:]
    print(save)
    return save
  else:
    return input()


def ask(printing):
  print(printing)
  return getinput()


class FakeTime:
  now = 0

  def time():
    # Advance clock a random amount.
    FakeTime.now = FakeTime.now + random.normalvariate(100, 10)
    return FakeTime.now


def program(testing=False):

  global global_testing
  global_testing = testing
  if testing:
    timer = FakeTime
  else:
    timer = time
  print('Welcome to Test timer!' + '\nHow many items are on this test?')
  questions = 'Not Digit'
  while not questions.isdigit():
    questions = getinput()
  questions = int(questions)
  answers = []
  for i in range(questions):
    answers.append((None, 0))

  print(
    "\nINSTRUCTIONS:\n",
    "Every time you _leave_ an item, even if you don't choose a new answer, enter it here, along with your answer (if any).\n",
    "The program will compute the duration since the previous item, and add it to your time spent on the item you entered."
  )

  ask("Press ENTER when ready to start timer.")
  print("Timer started.\n")
  problem_start_time = timer.time()

  while True:
    if False:
      print(
        "\nDEBUG: ",
        str(questions) + " items\n" + "\t#\tsecs\tanswer\n" +
        "\t-\t----\t------" + "\n\t" + "\n\t".join([
          f'{str(i+1)}\t{answers[i][1]}   \t{answers[i][0]}'
          for i in range(len(answers))
        ]), "\n")

    problem = 'None'
    while not ((problem.isdigit() and int(problem) <= questions) or
               (problem.lower() == 'stop')):
      problem = ask('problem number ("stop" to stop')
    if problem.lower() == 'stop':
      break
    else:
      now = timer.time()
      time_spent_sec = int(now - problem_start_time)
      # mark timer for next problem
      problem_start_time = now
      answer = ask("Answer (ENTER if skipped or unchanged): ")
      (old_answer, old_time_spent_sec) = answers[int(problem) - 1]
      answers[int(problem) - 1] = (answer if answer else old_answer,
                                   old_time_spent_sec + time_spent_sec)

  print('\n' * 50)
  print(
    "\n\t#\tsecs  \tanswer\n" + "\t-\t----\t------"
    "\n\t" + "\n\t".join([
      f'{str(i+1)}\t{answers[i][1]}   \t{answers[i][0]}'
      for i in range(len(answers))
    ]), "\n")


def main():
  program(testing=True)
