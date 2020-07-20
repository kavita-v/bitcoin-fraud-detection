import pandas as pd
from collections import defaultdict
import json

# Load transaction graph data from data files
graph_path = "./pp-data/txedges.dat"
df = pd.read_csv(graph_path, sep=r"\s+", names=['txid', 'inaddr', 'outaddr', 'weight'])

scam_tsv_path = "./pp-data/sample-scam-data-txid.tsv"
df_scam = pd.read_csv(scam_tsv_path, sep='\t', header=0)
fraud_txs = list(df_scam['addr'])

# Data Pre-processing
G = defaultdict(list)       # G represents graph
tx_node = defaultdict(list)
for row in df.itertuples():
    G[row.inaddr].append(row.outaddr)   #directed edge from inaddr to outaddr
    G[row.outaddr]                      #to ensure dangling nodes (out-degree=0) have an empty list
    tx_node[row.txid].append(row.outaddr)
    tx_node[row.txid].append(row.inaddr)

fraud_nodes = []
for txid in fraud_txs:
    fraud_nodes += tx_node[txid]

n = len(G)
print("No. of nodes in the graph: "+str(n))

m = len(fraud_nodes)
print("No. of preferred nodes (from public scam data): "+str(m))

v = dict() # v is normalized personalisation vector
v_i = float(1/m) # distribute personalisation weight equally amongst nodes involved in past public scams

for node in G.keys():
    if node in fraud_nodes:
        v[node] = v_i
    else:
        v[node] = 0

alpha = 0.85 # damping parameter
max_iter = 1000 # chosen constant
eps = float(10e-12)

y = dict.fromkeys(G, 1/n) #starting vector for PageRank score

outdeg = lambda node: len(G[node])

dangling_nodes = [node for node in G if outdeg(node)==0]
dangling_wts = v # taking dangling weights same as personalization weights

for run in range(max_iter):
    y_new = dict.fromkeys(y.keys(), 0)
    danglesum = alpha*sum(y[node] for node in dangling_nodes)
    
    for node in y:
        if node not in dangling_nodes:
            s = y[node]/outdeg(node) # contribution from one out-edge
            for nbr in G[node]:
                y_new[nbr] += alpha*s
        y_new[node] += danglesum*dangling_wts[node] + (1 - alpha)*v[node]
    
    # check convergence - L1 Norm
    err = sum([abs(y_new[node] - y[node]) for node in y])
    if (err < n*eps):
        norm = sum(y_new.values())
        z = dict((k, v / norm) for k, v in y_new.items())
        break

    y = y_new

# Check that PPR vector converged 
if (err > n*eps):
    raise Exception(f"Personalised PageRank did not converge in {max_iter} iterations.")

# Save PPR scores in descending order
ppr_scores = {k: v for k, v in sorted(z.items(), key=lambda item: item[1], reverse=True)}

res = open("./results/ppr-power-method-results.json", "w")
json.dump(ppr_scores, res)
res.close()
