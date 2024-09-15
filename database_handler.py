import sqlite3
import pickle
import networkx as nx

def graph6_to_iso_invariant(graph6):
  '''
  Computes the degree sequence and triangle sequence to create an isomorphism
  invariant for quick lookup times. Equivalent to using nx.fast_could_be_iso.
  '''
  
  G = nx.from_graph6_bytes(graph6.encode())

  d = G.degree()
  t = nx.triangles(G)
  props = [[d, t[v]] for v, d in d]
  props.sort()

  return str(props)

def db_write(conn, graph6, iso_invariant, num_nodes, num_edges,
             is_connected=None, is_tree=None, is_local=None, is_global=None,
             fer_group_encoded=None):
  
  if fer_group_encoded:
    fer = pickle.dumps(fer_group_encoded)
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
                 fer_group_encoded)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
               (graph6, iso_invariant, num_nodes, num_edges,
                is_connected, is_tree, is_local, is_global, fer))
  
  conn.commit()

def db_read(conn, id):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM graphs WHERE id = ?', (id,))
  row = cursor.fetchone()
  fer = row[-1]
  if fer:
    des_fer = pickle.loads(fer)
  
  return row[:-1], des_fer