
#importing libraries
import pandas as pd
import numpy as np

#reading the txedges.dat
col_names=['txID', 'in_addr', 'out_addr', 'weight'] 
df = pd.read_csv('txedges.dat',sep='\t',names=col_names, header=None)

lis_t=[] 
for i in range(len(df)):
  temp=[]
  temp.append(df['in_addr'][i])
  temp.append(df['out_addr'][i])
  lis_t.append(temp)
  
for j in range(len(lis_t)):
  if lis_t[j][0]==lis_t[j][1]:
    lis_t.remove(lis_t[j])
    
#Example of dict
#dic_t = {1: [2], 3: [1], 5: [4]}

old_dic_t={}
for k,v in lis_t:
  old_dic_t.setdefault(v,[]).append(k)
for i in old_dic_t:
  old_dic_t[i]=list(set(old_dic_t[i]))

dic_t={k: [] for k in range(42790)}
dic_t.update(old_dic_t)

#Adjacency Matrix
mat=[]
for i in range(43000):
  mat.append([0 for j in range(43000)])
for i in range(len(df)):
  if (df['in_addr'][i]==df['out_addr'][i]):
    print("Same vertex %d and %d" % (df['in_addr'][i],df['in_addr'][i]))
  mat[df['in_addr'][i]][df['out_addr'][i]]=1
  mat[df['out_addr'][i]][df['in_addr'][i]]=1

#DFS
def dfs(G, start, end):
    stack = [(start, [])]
    while (stack):
        state, cycle = stack.pop()
        for i in G[state]:
            if i in cycle:
                continue
            stack.append((i, cycle+[i]))
        if cycle and state == end:
            yield cycle
 
G = dic_t
cycles = [[u]+cycle  for u in G for cycle in dfs(G, u, u)]
print("Number of cycles:",len(cycles))
print("Cycles:")
print(cycles)
