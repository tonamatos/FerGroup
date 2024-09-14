from Fer_G import FerGroup, FerGroup_decoder
from sympy.combinatorics import PermutationGroup
from functools import cached_property

class Fer_group:
  '''
  Given a NetworkX colored_graph, it will generate the group of Fer objects.
  The list of generators includes all automorphisms and the one edge-replacements as Fer objects.
  If given a decode=([list of automorphisms arrays],[list of one edge-replacement arrays]),
  the constructor will assume this list contains all
  permutations corresponding to automorphisms and one edge-replacements in array form, and
  will use them to reconstruct the group instead of computing it from scratch. This is much
  faster than creating the group from scratch.
  If decode is empty, the constructor will call the FerGroup function to find the group.
  Once a Fer_group is created, the list of arrays that reconstructs the group can be created
  using the .encode() method.
  '''
  def __init__(self, colored_graph, encoded=None):
    if encoded:
      FGroup = FerGroup_decoder(colored_graph, encoded)
    else:
      FGroup = FerGroup(colored_graph)

    self.generators = list(FGroup.values()) # Set of Fer objects including Aut(G)
    self._encoded = encoded

  def __str__(self):
    if not self.generators:
      return 'Group is empty.'
    
    aut = self.automorphism
    non = self.non_aut

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
  
  @cached_property
  def group(self):
    return PermutationGroup(*[gen.seq_perm for gen in self.generators])
  
  @cached_property
  def automorphism(self):
    return [fer for fer in self.generators if fer.isTrivial()]
  
  @cached_property
  def non_aut(self):
    return [fer for fer in self.generators if not fer.isTrivial()]
  
  def encode(self): # Returns the list of generators in array form
    if self._encoded is not None:
      return self._encoded
    
    # Extract array forms of generators
    autom  = [fer.seq_perm.array_form for fer in self.automorphism] # Automorphisms
    nonaut = [fer.seq_perm.array_form for fer in self.non_aut]      # Non-automorphisms
    self._encoded = (autom, nonaut)
    return self._encoded