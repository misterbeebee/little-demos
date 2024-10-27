# From https://github.com/quchen/articles/blob/master/loeb-moeb.md
# Python port

for i in range(1):

  def isfunction(x):
    return (type(x) in [type(len), type(lambda: None)])

  def allof(f, *xs):
    return all(map(f, xs))

  def anyof(f, *xs):
    return any(map(f, xs))

  def isnt(f):
    return lambda x: not f(x)

  done = isnt(isfunction)

  def myprint(xs):
    print("\t-> ", "\t".join([str(x) if done(x) else "_" for x in xs]))

  def lazy(f, *deps):
    "Evaluate f(xs), only if dependencies (listed by index in xs) are resolved."

    def lazy_f(xs):
      if allof(done, *[xs[d] for d in deps]):
        return f(xs)
      else:
        return lazy(f, *deps)

    return lazy_f

  def loeb_unsafe(fs):
    "Loeb for lists, but doesn't detect dependency cycles."
    xs = fs[:]

    # THE IMPORTANT PART!
    while anyof(isnt(done), *xs):
      # 'if done(x) is special for Python: convert function to value, since
      # Python doesn't know how to evaluate/call a value like Haskell does.
      xs = [x if done(x) else x(xs) for x in xs]
    return xs

  def loeb_safe(fs):
    "Loeb for lists, stops when it detects a dependency cycle."
    xs = fs[:]

    # THE IMPORTANT PART!
    while not allof(done, *xs):
      myprint(xs)
      # 'if done(x) is special for Python: convert function to value, since
      # Python doesn't know how to evaluate/call a value like Haskell does.
      new_xs = [x if done(x) else x(xs) for x in xs]
      if list(filter(done, new_xs)) == list(filter(done, xs)):
        print("CYCLE DETECTED!")
        break
      xs = new_xs
    return xs

  def main():
    fs = [
      lazy(lambda xs: xs[1] + xs[2], 1, 2),
      lazy(lambda xs: xs[3] + 1, 3),
      lazy(lambda xs: xs[0] + 1, 0),
      lambda xs: 1,
      lazy(lambda xs: xs[5] + 1, 5),
      # unsafe!
      # lazy(lambda xs: xs[4] + 1, 4),
      lambda xs: 100,
      200
    ]

    print("safe:")
    myprint(loeb_safe(fs))
    print("\nunsafe:")
    myprint(loeb_unsafe(fs))


# main()
