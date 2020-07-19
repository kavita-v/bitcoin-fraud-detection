import pandas as pd
from collections import defaultdict
import json

# Load transaction graph data from data files
graph_path = "./pp-data/txedges.dat"
df = pd.read_csv(graph_path, sep=r"\s+", names=['txid', 'inaddr', 'outaddr', 'weight'])

scam_tsv_path = "./pp-data/scam-data-txid.tsv"
df_scam = pd.read_csv(scam_tsv_path, sep='\t', header=0)
fraud_nodes = list(df_scam['addr'])

# Data Pre-processing
G = defaultdict(list)       # G represents graph
for row in df.itertuples():
    G[row.inaddr].append(row.outaddr)   #directed edge from inaddr to outaddr
    G[row.outaddr]                      #to ensure dangling nodes (out-degree=0) have an empty list

n = len(G)
print("No. of nodes in the graph: "+str(n))

m = len(df_scam)
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

for run in range(max_iter):
    err = float(0)

    for i in G:
        s = sum(y[j]/outdeg(j) for j in G.keys() if (i in G[j]))
        y_i_new = v[i] + alpha*s
        err += abs(y_i_new - y[i])
        y[i] = y_i_new

    if (err < eps):
        norm = sum(y.values())
        z = dict((k, v / norm) for k, v in y.items())
        break

# Check that PPR vector converged 
if (err > eps):
    raise Exception(f"Personalised PageRank did not converge in {max_iter} iterations.")

# Save PPR scores in descending order
ppr_scores = {k: v for k, v in sorted(z.items(), key=lambda item: item[1], reverse=True)}

res = open("./results/sample-ppr-results.json", "w")
json.dump(ppr_scores, res)
res.close()
