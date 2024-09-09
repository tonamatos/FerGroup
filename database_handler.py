import sqlite3
import pickle

def db_write(conn, graph_g6, num_nodes, num_edges, is_connected, is_tree=None, is_local=None, is_global=None, fer=None):
  if fer:
    s_fer = pickle.dumps(fer)
  else:
    s_fer = None
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO graphs
                 (graph_g6,
                 num_nodes,
                 num_edges,
                 is_connected,
                 is_tree,
                 is_local,
                 is_global,fer)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
               (graph_g6, num_nodes, num_edges, is_connected, is_tree, is_local, is_global, s_fer))
  conn.commit()

def db_read(conn, id):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM graphs WHERE graph_g6 = ?', (id,))
  row = cursor.fetchone()
  fer = row[-1]
  if fer:
    des_fer = pickle.loads(fer)
  
  return row