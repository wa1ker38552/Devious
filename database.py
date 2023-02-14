import json

class Database:
  def __init__(self, path=None):
    if path is None:
      self.path = 'config.json'
    else:
      self.path = path

  def load(self):
    with open(self.path, 'r') as file:
      return json.loads(file.read())

  def set_key(self, key, value):
    data = self.load()
    data[key] = value
    self.save(data)
  
  def save(self, data):
    with open(self.path, 'w') as file:
      file.write(json.dumps(data, indent=2))
