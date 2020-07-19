import pandas as pd
import csv

scam_tsv_path = "./pp-data/scam-data-txh.tsv"
df_scam = pd.read_csv(scam_tsv_path, sep='\t', header=0)
spam_txn = list(df_scam['txid'])

txh_dataset_path = "../dataset/txh.dat"

df_txh = pd.read_csv(txh_dataset_path, header=None , names=['txID','hash'], sep= "\\t", quotechar='"')#, encoding='utf-8')

spam_txid = []

for row in df_txh.itertuples():
    print("Checking row "+ str(row.txID))
    if row.hash in spam_txn:
        spam_txid.append(row.txID)
        print("FOUND A MATCH")

with open('./pp-data/scam-data-txid.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerow(['addr'])
    print("WRITING INTO FILE...")
    for txid in spam_txid:
        tsv_output.writerow([txid])