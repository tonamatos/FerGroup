import pickle
import networkx as nx
from fer_group import Fer_group
import sqlite3

def ferGroupS(graph6):
  G = nx.from_graph6_bytes(graph6.encode())

  fer_group_e = Fer_group(G).encode() # Encode

  fer_group_s = pickle.dumps(fer_group_e) # Serialize

  return fer_group_s

def isoInvariant(graph):
  '''
  Computes the degree sequence and triangle sequence to create an isomorphism
  invariant for quick lookup times. Equivalent to using nx.fast_could_be_iso.
  '''

  d = graph.degree()
  t = nx.triangles(graph)
  props = [[d, t[v]] for v, d in d]
  props.sort()

  return str(props)

def db_write(conn, graph6, iso_invariant, num_nodes, num_edges,
             is_connected=None, is_tree=None, is_local=None, is_global=None,
             fer_group=None):
  
  if fer_group:
    fer = pickle.dumps(fer_group)
  else:
    fer = None
    
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO graphs
                 (graph6,
                 iso_invariant,
                 num_nodes,
                 num_edges,
                 is_connected,
                 is_tree,
                 is_local,
                 is_global,
                 fer_group)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
               (graph6, iso_invariant, num_nodes, num_edges,
                is_connected, is_tree, is_local, is_global, fer))
  
  conn.commit()

def db_fetch(graph6, iso_invariant):
  conn = sqlite3.connect('databases/graphs.db')
  cursor = conn.cursor()

  # Try to find exact match
  cursor.execute('SELECT * FROM graphs WHERE graph6 = ?', (graph6,))
  row = cursor.fetchone()
  if row:
    return row
  
  # Use isomorphism invariants to find good matches
  