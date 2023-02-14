import copy

def filter(original):
  banned = open('assets/blacklist.txt', 'r').read().split('\n')
  reference = copy.copy(original)
  for word in banned:
    if word in original.lower() or word in ''.join(original.lower().split()):
      for ow in original.split():
        if ow.lower() == word:
          original = original.replace(ow, '#'*len(word))
      if original != reference:
        return original
      else:
        return '#'*len(original)
  return original
