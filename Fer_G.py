from itertools import combinations
from networkx.algorithms import isomorphism
from feasible_edge_replacements import Feasible_edge_replacement as Fer
from sympy.combinatorics.permutations import Permutation as Perm

def edge_replace(graph, old_edge, new_edge):
  new_graph = graph.copy()
  if set(old_edge) == set(new_edge):
    return new_graph
  new_graph.remove_edge(*old_edge)
  new_graph.add_edge(*new_edge)
  return new_graph

def iso_invert(iso):
  '''
  Inverts an isomorphism given as hash_map {0:,1:,...}
  '''
  inverse = {}
  for key, value in iso.items():
    inverse[value] = key
  return inverse

def isFer(colored_graph, old_edge, new_edge, allIso=False):
  '''
  Given NetworkX colored_graph and old_edge={i,j}, new_edge={x,y}, decides
  if removing old_edge and adding new_edge produces a graph color-
  isomorphic to the original graph. Returns some isomorphism if True
  and False otherwise. Setting allIso=True, returns all color-isomorphisms
  that correspond to the edge-replacement.
  '''
  color_match = lambda x, y: x['color'] == y['color']
  graph_replaced = edge_replace(colored_graph, old_edge, new_edge)
  GM = isomorphism.GraphMatcher(colored_graph, graph_replaced, node_match=color_match)

  # Option to return all isomorphisms
  if allIso:
    list_all_iso = [iso_invert(iso) for iso in GM.subgraph_isomorphisms_iter()]
    if list_all_iso:
      return list_all_iso
    else:
      return False

  # Else, just return the first one that the GraphMatcher finds.
  try:
    first_iso = iso_invert(next(GM.subgraph_isomorphisms_iter()))
    return first_iso
  except StopIteration:
    return False

def FerGroup(colored_graph):
  '''
  Given a NetworkX colored_graph, returns the group of all Fer objects associated to a single
  feasible edge-replacement as a hash map, linking permutations to their Fer object.
  Whose sequence has length 1. If this group generates the
  maximum possible group or not will determine of colored_graph is a colored amoeba.
  '''

  edges = colored_graph.edges()
  nodes = colored_graph.nodes()

  # If graph is not fully colored, we assume all vertices are the same color.
  if not hasattr(nodes[0], 'color'):
    for node in colored_graph.nodes():
      colored_graph.nodes[node]['color'] = 'black'

  n = len(nodes)
  alledges = combinations(nodes, 2)
  nonedges = [(x, y) for (x, y) in alledges if not (x, y) in edges and not (y, x) in edges]
  
  id_per = Perm(n-1) # Identity is always feasible.
  fers = {tuple(id_per) : Fer(old_edge={0,1}, new_edge={0,1}, permutation=id_per)}

  # Add automorphisms to trivial edge-replacement, as these are always fers.
  automorphisms = isFer(colored_graph, old_edge={0,1}, new_edge={0,1}, allIso=True)
  #print("Found",len(automorphisms),"automorphisms.")
  for iso in automorphisms:
    iso_tuple = tuple(iso[i] for i in range(len(iso)))
    try:
      fers[iso_tuple] = Fer(old_edge={0,1}, new_edge={0,1}, permutation=Perm(iso_tuple))
    except:
      print(iso_tuple)

  # Iterate over all possible edge-replacements. If feasible, add to hash_map.
  for old_edge in edges:
    for new_edge in nonedges:
      iso = isFer(colored_graph, old_edge, new_edge)
      if iso:
        iso_tuple = tuple(iso[i] for i in range(len(iso)))
        fers[iso_tuple] = Fer(old_edge=set(old_edge), new_edge=set(new_edge), permutation=Perm(iso_tuple))

  return fers