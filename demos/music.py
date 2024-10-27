import time
import math
import random
from replit import audio


def play_note(stepsAboveA):
  pitch = 220 * math.pow(2, stepsAboveA / 12)
  print(f'step: A+ {stepsAboveA}   pitch: {pitch}')

  source = audio.play_tone(
    duration=100,  #ms, but seems ignored
    pitch=pitch,
    wave_type=0,
    does_loop=False,
    loop_count=0,
    volume=1)
  return source


def main():

  print("[12345678]th, or multiple '45' for random?")

  options = (input())
  while True:
    nthToInterval = {
      1: 0,
      2: 2,
      3: 4,
      4: 5,  # half-step
      5: 7,
      6: 9,
      7: 11,
      8: 12  # half-step
    }
    nth = int(random.sample(options, 1)[0])
    print("Base")
    base = random.randint(0, 1 * 8 - 1)
    source = play_note(base)

    #   print("sleep")
    time.sleep(1)

    #    print("pause")
    source.set_paused(True)

    time.sleep(1)

    print("Interval")
    source = play_note(base + nthToInterval[nth])

    #  print("sleep")
    time.sleep(1)

    #   print("pause")
    source.set_paused(True)

    #    print("sleep")
    time.sleep(3)
