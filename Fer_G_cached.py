from fer_group import Fer_group
from database_handler import db_fetch
import pickle
from sympy.combinatorics.permutations import Permutation as Perm 

def Fer(graph, cached=True):
  '''
  Computes the Fer group either by creating the object from scratch or retrieving
  and reconstructing from databasaes/graphs.db
  '''
  if cached:
    fetch = db_fetch(graph)
    if fetch:
      row, iso_mapping = fetch
      iso = Perm([iso_mapping[key] for key in sorted(iso_mapping)])
      print("Relabeling by",iso)
      encoded = pickle.loads(row[-1])
      autom, nonaut = encoded
      autom   = [(iso*Perm(array)*iso**(-1)).array_form for array in autom]
      nonaut  = [(iso*Perm(array)*iso**(-1)).array_form for array in nonaut]
      encoded = (autom, nonaut)

      return Fer_group(graph, encoded)
  
  return Fer_group(graph)