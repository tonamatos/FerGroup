import pickle
import networkx as nx
from networkx.algorithms import isomorphism
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

def db_fetch(graph):
  '''
  Attempts to find the networkx object graph in the database.
  If it does, it returns the db row and the relabing,
  in case an isomorphic copy was found instead.
  '''
  try:
    conn = sqlite3.connect('databases/graphs.db')
  except sqlite3.Error as e:
    print(f"Error connecting to the database: {e}")
    return
  
  cursor = conn.cursor()

  # Try to find exact match
  graph6 = nx.to_graph6_bytes(graph).decode('utf-8')[10:-1]

  cursor.execute('SELECT * FROM graphs WHERE graph6 = ?', (graph6,))
  row = cursor.fetchone()
  if row:
    conn.close()

    # The graph may be the same but the labeling must be computed
    H = nx.from_graph6_bytes(row[1].encode())
    GM = isomorphism.GraphMatcher(graph, H)
    _ = GM.is_isomorphic()
    iso_mapping = GM.mapping

    print("Exact match found in database.")
    return row, iso_mapping

  # NOTE: Since graph6 is a canonization, everything below this line might never be executed

  # Compute isomorphic invariants
  inv = isoInvariant(graph)

  # Find all graphs with the same invariant
  cursor.execute('SELECT * FROM graphs WHERE iso_invariant = ?', (inv,))
  rows = cursor.fetchall()
  conn.close()

  if rows:
    print("Found",len(rows),"graph(s) with the same isomorphism invariants in database.")
  else:
    return

  # Find exact match within candidates
  for row in rows:
    H = nx.from_graph6_bytes(row[1].encode())

    GM = isomorphism.GraphMatcher(graph, H)
    if GM.is_isomorphic():
      iso_mapping = GM.mapping
      return row, iso_mapping

  print("No match found in database.")