import pandas as pd
import csv

scam_tsv_path = "./pp-data/scam-data-txh.tsv"
df_scam = pd.read_csv(scam_tsv_path, sep='\t', header=0)
spam_txn = list(df_scam['txid'])

txh_dataset_path = "../dataset/txh.dat.gz"

df_txh = pd.read_csv(txh_dataset_path, compression='gzip', header=None , sep= "\\t", quotechar='"', engine='python')

spam_txid = []

for row in df_txh.head().itertuples():
    if row.hash in spam_txn:
        spam_txid.append(row.txID)

with open('./pp-data/scam-data-txid.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerow(['addr'])
    for txid in spam_txid:
        tsv_output.writerow([txid])