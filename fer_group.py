from Fer_G import FerGroup
from sympy.combinatorics import PermutationGroup

class Fer_group:
  '''
  Given a NetworkX colored_graph, it will generate the group of Fer objects as a generator object.
  It includes information that helps decide if the input is a colored amoeba or not.
  '''
  def __init__(self, colored_graph):
    FGroup = FerGroup(colored_graph)
    self.generators = list(FGroup.values()) # Set of Fer objects.

  def __str__(self):
    if not self.generators:
      return 'Group is empty.'
    
    aut = self.automorphism()
    non = self.non_aut()

    if aut:
      table = 'Automorphism generators\n'
      for fer in aut:
        table = table+str(fer)+'\n'
      table = table + '\n'
    else:
      table = 'No automorphisms found.\n'

    if non:
      table = table + 'Non-trivial Fer object generators\n'
      for fer in non:
        table = table+str(fer)+'\n'
    else:
      table = table + 'No non-trivial Fer objects found.\n'
    return table
  
  def group(self):
    return PermutationGroup(self.generators)
  
  def automorphism(self):
    return [fer for fer in self.generators if fer.isTrivial()]
  
  def non_aut(self):
    return [fer for fer in self.generators if not fer.isTrivial()]
