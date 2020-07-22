# Anomaly Detection in Bitcoin Transaction Network
This project explores some basic anomaly detection techniques in the Bitcoin transaction network. Please look at the article in [this](https://medium.com/@kavita.vaishnaw/anomaly-detection-in-bitcoin-transaction-network-3f1defdc9ef2?source=friends_link&sk=25fe87867d40b2ee427dc709520e70ae) link to find more supporting information.

## Creating the Bitcoin Transaction Network
The Bitcoin dataset used in this project can be found in https://senseable2015-6.mit.edu/bitcoin/. To make the network using this data, follow this repo: https://github.com/dkondor/txedges. After processing the Bitcoin data, the network dataset used in this project can be found in txedges.dat in pp-data. The data is tab separated list of edges having 4 columns: transaction id, transaction input address id, transaction output address id, weight. Hence, addresses act as nodes with transactions as directed edges weighted by transaction id's and transaction weights(in satoshis).

## Contributors:
- [Kavita Vaishnaw](https://github.com/kavita-v "Kavita's GitHub Profile")
- [Kanishk Kalra](https://github.com/kanishkkalra11 "Kanishk's GitHub Profile")
- [Mohit Mina](https://github.com/mohitmina "Mohit's GitHub Profile")
