def scanner(name, function):
   list(map(function, open(name, 'r')))
