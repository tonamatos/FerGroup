class FerGroup:
  '''
  Given a NetworkX colored_graph, it will generate the group of Fer objects as a generator object.
  It includes information that helps decide if the input is a colored amoeba or not.
  '''
  def __init__(self, colored_graph):
    self.fers   = {}   # Set of Fer objects. (Usually the generators.)
    self._order = None # Order of group. None=unknown.

  def __str__(self):
    if not self.fers:
      return 'Group is empty.'
    
    if self._order:
      order = str(self._order)
    else:
      order = '?'
    
    table = 'Order = '+order+'\t\n\n'
    for fer in self.fers:
      if fer.isTrivial:
        table = table+str(fer)+'(automorphism)'+'\t\n'
      table = table+str(fer)+'\t\n'
    return table