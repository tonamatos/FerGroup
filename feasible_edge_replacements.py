from sympy.combinatorics.permutations import Permutation

class Feasible_edge_replacement:
  '''
  A sequence of Feasable Edge Replacements perm_seq::(permutation : old_edge -> new_edge)...()
  Can be concatenated with *, hashed, iterated, printed, and added individual replacements.
  '''
  class _Individual_Fer:
    def __init__(self, old_edge, new_edge):
      if not isinstance(old_edge, set) or not isinstance(new_edge, set):
        raise TypeError("Edges must be sets (not tuples).")

      self.old_edge = old_edge
      self.new_edge = new_edge

    def tex(self):
      if self.old_edge == self.new_edge:
        return '(\\emptyset \\to \\emptyset)'
      i, j = self.old_edge
      x, y = self.new_edge
      return f"({i}\\ {j} \\to {x}\\ {y})"

    def __add__(self, other): # Shifts edge labels by other (int).
      i, j = self.old_edge
      x, y = self.new_edge
      return Feasible_edge_replacement._Individual_Fer({i + other, j + other}, {x + other, y + other})

    def __str__(self):
      if self.isTrivial:
        return '(0 -> 0)'
      
      i, j = self.old_edge
      x, y = self.new_edge
      return f"({i} {j} -> {x} {y})"

    def isTrivial(self):
      return self.old_edge == self.new_edge


    def _update(self, permutation):
      '''
      Updates the labels of the edge replacement according to the given permutation.
      The intended use is when multiplying with a sequence on the left. Can also use
      conjugation with inverse, but this seems a little faster, since we only need
      to invert once (and conjugation would compute three inverses).
      '''
      old_i, old_j = self.old_edge
      old_x, old_y = self.new_edge

      # Make sure Permutation is the right size:
      m = max([old_i, old_j, old_x, old_y])
      permutation = Permutation(m)*permutation**(-1)

      # Update new values after permuting.
      p_list = permutation.list()

      new_i = p_list[old_i]
      new_j = p_list[old_j]
      new_x = p_list[old_x]
      new_y = p_list[old_y]
      return Feasible_edge_replacement._Individual_Fer({new_i, new_j}, {new_x, new_y})

  def __init__(self, old_edge=None, new_edge=None, permutation=None, sequence=None):
    if sequence:
      self.sequence = sequence
      self.seq_perm = permutation
    else:
      ind_fer_to_add = self._Individual_Fer(old_edge, new_edge)
      self.sequence = [ind_fer_to_add]
      self.seq_perm = permutation

  def __add__(self, other): # Shifts all labels in object by other.
    new_seq = [fer + other for fer in self.sequence]
    old_per = self.seq_perm
    new_siz = old_per.size + other
    conj    = Permutation([im%new_siz for im in range(other, new_siz + other)])
    new_per = (Permutation(old_per, size=new_siz))^conj

    return Feasible_edge_replacement(permutation=new_per, sequence=new_seq)

  def tex(self): # Creates tex-formatted str for use in manim library.
    if not self.sequence:
      return '[]'
    string = ''
    for ind_fer in self.sequence:
      string = string + ind_fer.tex()
    return string

  def __str__(self): # Prints in format permutation::(a -> b)(...)
    if not self.sequence:
      return '[]'
    string = ''
    for ind_fer in self.sequence:
      string = string + str(ind_fer)
    return f'{str(self.seq_perm):>24}' + ' : ' + string

  def isTrivial(self):
    if self.sequence[0].isTrivial():
      return True
    return False

  def __len__(self):
    return len(self.sequence)

  def _simplify_once(self):
    '''
    Shortens the length of the sequence by removing repetitions or replacements that cancel out.
    '''
    new_seq = [fer for fer in self.sequence]
    for i in range(len(new_seq)):

      # Don't add fers that cancel out.
      if i+1 < len(new_seq) and new_seq[i].new_edge == new_seq[i+1].old_edge and new_seq[i].old_edge == new_seq[i+1].new_edge:
        new_seq.pop(i)
        new_seq.pop(i)
      if i+1 < len(new_seq) and new_seq[i].new_edge == new_seq[i+1].old_edge: # (e->f)(f->g)=(e->g)
        left_old  = new_seq[i].old_edge
        right_new = new_seq[i+1].new_edge
        new_seq.pop(i)
        new_seq.pop(i)
        new_seq.insert(i, self._Individual_Fer(left_old, right_new))
      if i+1 < len(new_seq) and new_seq[i].old_edge == new_seq[i+1].new_edge: # (f->g)(e->f)=(e->g)
        left_new  = new_seq[i].new_edge
        right_old = new_seq[i+1].old_edge
        new_seq.pop(i)
        new_seq.pop(i)
        new_seq.insert(i, self._Individual_Fer(right_old, left_new))
    
    # Trivial edge replacement doesn't get added.
    new_seq = [fer for fer in new_seq if fer.old_edge != fer.new_edge]

    if not new_seq:
      new_seq = [self._Individual_Fer({0,1}, {0,1})]
    
    self.sequence = new_seq

  def _simplify(self, times=0):
    '''
    Iterates the _simplify method several times. Default times=0 iterates until no change in length is made.
    '''
    if times == 0:
      old_length = len(self) + 1
      while len(self) < old_length:
        old_length = len(self)
        self._simplify_once()

    else:
      for i in range(times):
        self._simplify_once()

  def __mul__(self, other): # Concatenates to Fers and updates labels correctly.
    left_perm  = self.seq_perm
    right_perm = other.seq_perm
    left_seq   = self.sequence
    right_seq  = [fer._update(left_perm) for fer in other.sequence]
    new_fer = Feasible_edge_replacement(old_edge=None, new_edge=None, permutation=left_perm*right_perm, sequence=left_seq+right_seq)
    new_fer._simplify()
    return new_fer

  def __getitem__(self, index):
    return self.sequence[index]

  def __iter__(self):
    return iter(self.sequence)