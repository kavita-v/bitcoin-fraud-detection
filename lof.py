# make necessary imports
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.neighbors import LocalOutlierFactor

# read the bitcoin transactions data
col_names=['txID', 'in_addr', 'out_addr', 'weight'] #weights are in satoshis
df = pd.read_csv('pp-data/txedges.dat',sep='\t',names=col_names, header=None)

# make features for lof calculation: in-degree, out-degree, mean incoming transaction value, mean outgoing transaction value, clustering coefficient

f_indeg = dict(Counter(df['out_addr'])) #in-degree

f_outdeg = dict(Counter(df['in_addr'])) #out-degree

group = df.groupby('out_addr')
f_meanin = dict(group.apply(lambda x: x['weight'].mean())) #mean incoming transaction value

group = df.groupby('in_addr')
f_meanout = dict(group.apply(lambda x: x['weight'].mean())) #mean outgoing transaction value

group = df.groupby('in_addr')
ni = dict(group.apply(lambda x: list(x['out_addr'])))
ci = {}
for key in list(ni.keys()):
    k = len(list(ni[key]))
    n = 0
    for item in list(ni[key]):
        for item1 in list(ni[key]):
            try:
                if item1 in list(ni[item]):
                    n += 1
            except:
                continue
    try:
        ci[key] = n/(k*(k-1))
    except:
        ci[key] = n
f_clustercoeff = ci #clustering coefficient, see https://en.wikipedia.org/wiki/Clustering_coefficient for reference

# make processed dataset for lof calcultaion
fs = [f_indeg, f_outdeg, f_meanin, f_meanout, f_clustercoeff]
users = list(set(list(f_outdeg.keys())+list(f_indeg.keys())))
f = {}
for k in users:
    l = []
    for feature in fs:
        try:
            l.append(feature[k])
        except:
            l.append(0)
    f[k] = l
df2 = pd.DataFrame([{"address": addr, "in-degree": indeg, "out-degree": outdeg, "mean-incoming-transaction-value": meanin, "mean-outgoing-transaction-value": meanout, "clustering-coefficient": clustercoeff} for addr, [indeg,outdeg,meanin,meanout,clustercoeff] in f.items()])

# calulate lof using sklearn
clf = LocalOutlierFactor(n_neighbors=20)
o1 = list(clf.fit_predict(df2[['in-degree','out-degree','mean-incoming-transaction-value','mean-outgoing-transaction-value','clustering-coefficient']]))

# find outliers
o2 = list(df2['address'])
indices = [i for i, x in enumerate(o1) if x == -1]
outliers = []
for i in range(len(indices)):
    outliers.append(o2[indices[i]])
print(outliers)