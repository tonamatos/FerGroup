import sqlite3
import pickle
import networkx as nx

def graph6_to_iso_invariants(graph6):
  G = nx.from_graph6_bytes(graph6.encode())

  degree_seq   = sorted([d for n, d in G.degree()], reverse=True)
  triangle_seq = nx.triangles(G).values()

  return degree_seq, triangle_seq

def db_write(conn, graph6, degree_seq, triangle_seq, num_nodes, num_edges,
             is_connected=None, is_tree=None, is_local=None, is_global=None,
             fer_group_encoded=None):
  
  if fer_group_encoded:
    fer = pickle.dumps(fer_group_encoded)
  else:
    fer = None
    
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO graphs
                 (graph6,
                 degree_seq,
                 triangle_seq,
                 num_nodes,
                 num_edges,
                 is_connected,
                 is_tree,
                 is_local,
                 is_global,
                 fer_group_encoded)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
               (graph6, degree_seq, triangle_seq, num_nodes, num_edges,
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